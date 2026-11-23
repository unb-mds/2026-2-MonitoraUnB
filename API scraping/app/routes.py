"""
Rotas da API REST para consulta e gerenciamento das disciplinas,
professores e turmas do SIGAA UnB.
"""

import math
import logging
import re
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db, SessionLocal
from app.models import Departamento, Disciplina, Professor, Turma, ScrapingLog
from app.schemas import (
    DepartamentoResponse,
    DisciplinaResponse,
    DisciplinaEquivalente,
    DisciplinaComDepartamento,
    ProfessorResponse,
    ProfessorComDisciplinas,
    TurmaResponse,
    ScrapingRequest,
    ScrapingLogResponse,
    ScrapingStatusResponse,
    EstatisticasResponse,
)
from app.scraper import SigaaScraper, executar_scraping, sincronizar_departamentos

logger = logging.getLogger(__name__)

router = APIRouter()


# =============================================================================
# BACKGROUND TASK HELPER
# =============================================================================

async def _executar_scraping_background(
    log_id: int,
    nivel: str,
    tipo: int,
    departamento_sigaa_id: Optional[int],
    buscar_professores: bool,
    ano: Optional[str],
    periodo: Optional[str],
):
    """Executa a rotina de scraping em background utilizando uma nova sessão de banco."""
    db = SessionLocal()
    try:
        await executar_scraping(
            db=db,
            log_id=log_id,
            nivel=nivel,
            tipo=tipo,
            departamento_sigaa_id=departamento_sigaa_id,
            buscar_professores=buscar_professores,
            ano=ano,
            periodo=periodo,
        )
    except Exception as e:
        logger.error(f"Erro na execução da background task de scraping: {e}")
    finally:
        db.close()


# =============================================================================
# DISCIPLINAS
# =============================================================================

@router.get("/disciplinas", response_model=dict, tags=["Disciplinas"])
def listar_disciplinas(
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(50, ge=1, le=200, description="Itens por página"),
    codigo: Optional[str] = Query(None, description="Filtrar por código (busca parcial)"),
    nome: Optional[str] = Query(None, description="Filtrar por nome (busca parcial)"),
    nivel: Optional[str] = Query(None, description="Filtrar por nível de ensino"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo"),
    departamento_id: Optional[int] = Query(None, description="Filtrar por ID do departamento"),
    professor_nome: Optional[str] = Query(None, description="Filtrar por nome de docente ministrante"),
    db: Session = Depends(get_db),
):
    """
    Lista disciplinas com paginação, filtros e seus respectivos professores associados.
    """
    query = db.query(Disciplina)

    if codigo:
        query = query.filter(Disciplina.codigo.ilike(f"%{codigo}%"))
    if nome:
        query = query.filter(Disciplina.nome.ilike(f"%{nome}%"))
    if nivel:
        query = query.filter(Disciplina.nivel.ilike(f"%{nivel}%"))
    if tipo:
        query = query.filter(Disciplina.tipo.ilike(f"%{tipo}%"))
    if departamento_id:
        query = query.filter(Disciplina.departamento_id == departamento_id)
    if professor_nome:
        query = query.join(Disciplina.professores).filter(Professor.nome.ilike(f"%{professor_nome}%"))

    total = query.distinct().count()
    pages = math.ceil(total / per_page) if total > 0 else 1

    disciplinas = (
        query.distinct()
        .order_by(Disciplina.codigo)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
        "items": [DisciplinaResponse.model_validate(d) for d in disciplinas],
    }


@router.get("/disciplinas/codigo/{codigo}", response_model=list[DisciplinaComDepartamento], tags=["Disciplinas"])
async def buscar_por_codigo(
    codigo: str,
    buscar_detalhes: bool = Query(
        True,
        description="Se True, busca equivalências e ementa no SIGAA caso ainda não estejam no banco",
    ),
    db: Session = Depends(get_db),
):
    """
    Busca disciplinas pelo código (exato ou parcial) trazendo:
    - Departamento
    - Turmas (com horários, vagas e locais)
    - Professores
    - Ementa
    - Pré-requisitos e Co-requisitos
    - Expressão de equivalências e lista das disciplinas equivalentes
    """
    disciplinas = (
        db.query(Disciplina)
        .filter(Disciplina.codigo.ilike(f"%{codigo}%"))
        .order_by(Disciplina.codigo)
        .all()
    )
    if not disciplinas:
        raise HTTPException(status_code=404, detail="Nenhuma disciplina encontrada com esse código")

    scraper = None
    respostas = []

    try:
        for disc in disciplinas:
            # Se pedido e ainda não tiver detalhes no banco, busca no SIGAA
            if buscar_detalhes and disc.equivalencias is None and disc.ementa is None:
                if scraper is None:
                    scraper = SigaaScraper()
                try:
                    detalhes = await scraper.buscar_detalhes_disciplina(
                        codigo=disc.codigo,
                        nivel=disc.nivel or "G",
                    )
                    if detalhes:
                        disc.pre_requisitos = detalhes.get("pre_requisitos")
                        disc.co_requisitos = detalhes.get("co_requisitos")
                        disc.equivalencias = detalhes.get("equivalencias")
                        disc.ementa = detalhes.get("ementa")

                        # Cadastrar disciplinas equivalentes que ainda não estejam no banco
                        for eq_item in detalhes.get("disciplinas_equivalentes", []):
                            eq_cod = eq_item["codigo"]
                            eq_nome = eq_item.get("nome")
                            if eq_nome:
                                existing_eq = db.query(Disciplina).filter_by(codigo=eq_cod).first()
                                if not existing_eq:
                                    db.add(Disciplina(codigo=eq_cod, nome=eq_nome, nivel=disc.nivel))

                        db.commit()
                        db.refresh(disc)
                except Exception as e:
                    logger.warning(f"Não foi possível obter detalhes de {disc.codigo} no SIGAA: {e}")

            item_resp = DisciplinaComDepartamento.model_validate(disc)

            # Extrair a lista de disciplinas equivalentes estruturadas
            eq_list = []
            if disc.equivalencias:
                codigos_eq = re.findall(r"\b[A-Z]{2,6}\d{3,6}\b", disc.equivalencias)
                vistos = set()
                for cod_eq in codigos_eq:
                    if cod_eq != disc.codigo and cod_eq not in vistos:
                        vistos.add(cod_eq)
                        eq_db = db.query(Disciplina).filter_by(codigo=cod_eq).first()
                        nome_eq = eq_db.nome if eq_db else None
                        eq_list.append(DisciplinaEquivalente(codigo=cod_eq, nome=nome_eq))

            item_resp.disciplinas_equivalentes = eq_list
            respostas.append(item_resp)

    finally:
        if scraper:
            await scraper.close()

    return respostas


@router.get("/disciplinas/{disciplina_id}", response_model=DisciplinaComDepartamento, tags=["Disciplinas"])
async def obter_disciplina_por_id(
    disciplina_id: int,
    buscar_detalhes: bool = Query(
        True,
        description="Se True, busca equivalências e ementa no SIGAA caso ainda não estejam no banco",
    ),
    db: Session = Depends(get_db),
):
    """Busca detalhes de uma disciplina pelo seu ID interno, incluindo equivalências e ementa."""
    disciplina = db.query(Disciplina).filter_by(id=disciplina_id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

    if buscar_detalhes and disciplina.equivalencias is None and disciplina.ementa is None:
        scraper = SigaaScraper()
        try:
            detalhes = await scraper.buscar_detalhes_disciplina(
                codigo=disciplina.codigo,
                nivel=disciplina.nivel or "G",
            )
            if detalhes:
                disciplina.pre_requisitos = detalhes.get("pre_requisitos")
                disciplina.co_requisitos = detalhes.get("co_requisitos")
                disciplina.equivalencias = detalhes.get("equivalencias")
                disciplina.ementa = detalhes.get("ementa")

                for eq_item in detalhes.get("disciplinas_equivalentes", []):
                    eq_cod = eq_item["codigo"]
                    eq_nome = eq_item.get("nome")
                    if eq_nome:
                        existing_eq = db.query(Disciplina).filter_by(codigo=eq_cod).first()
                        if not existing_eq:
                            db.add(Disciplina(codigo=eq_cod, nome=eq_nome, nivel=disciplina.nivel))

                db.commit()
                db.refresh(disciplina)
        except Exception as e:
            logger.warning(f"Não foi possível obter detalhes de {disciplina.codigo} no SIGAA: {e}")
        finally:
            await scraper.close()

    item_resp = DisciplinaComDepartamento.model_validate(disciplina)
    eq_list = []
    if disciplina.equivalencias:
        codigos_eq = re.findall(r"\b[A-Z]{2,6}\d{3,6}\b", disciplina.equivalencias)
        vistos = set()
        for cod_eq in codigos_eq:
            if cod_eq != disciplina.codigo and cod_eq not in vistos:
                vistos.add(cod_eq)
                eq_db = db.query(Disciplina).filter_by(codigo=cod_eq).first()
                nome_eq = eq_db.nome if eq_db else None
                eq_list.append(DisciplinaEquivalente(codigo=cod_eq, nome=nome_eq))

    item_resp.disciplinas_equivalentes = eq_list
    return item_resp


# =============================================================================
# PROFESSORES
# =============================================================================

@router.get("/professores", response_model=dict, tags=["Professores"])
def listar_professores(
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(50, ge=1, le=200, description="Itens por página"),
    nome: Optional[str] = Query(None, description="Filtrar por nome do docente (busca parcial)"),
    departamento_id: Optional[int] = Query(None, description="Filtrar por ID do departamento"),
    db: Session = Depends(get_db),
):
    """
    Lista professores cadastrados com paginação e filtros.
    """
    query = db.query(Professor)

    if nome:
        query = query.filter(Professor.nome.ilike(f"%{nome}%"))
    if departamento_id:
        query = query.filter(Professor.departamento_id == departamento_id)

    total = query.count()
    pages = math.ceil(total / per_page) if total > 0 else 1

    professores = (
        query.order_by(Professor.nome)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
        "items": [ProfessorResponse.model_validate(p) for p in professores],
    }


@router.get("/professores/{professor_id}", response_model=ProfessorComDisciplinas, tags=["Professores"])
def obter_professor_por_id(professor_id: int, db: Session = Depends(get_db)):
    """Retorna detalhes do professor e a lista de disciplinas que ele ministra."""
    professor = db.query(Professor).filter_by(id=professor_id).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    return professor


@router.get("/professores/{professor_id}/disciplinas", response_model=list[DisciplinaResponse], tags=["Professores"])
def listar_disciplinas_do_professor(professor_id: int, db: Session = Depends(get_db)):
    """Retorna todas as disciplinas ministradas por um professor específico."""
    professor = db.query(Professor).filter_by(id=professor_id).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    return [DisciplinaResponse.model_validate(d) for d in professor.disciplinas]


# =============================================================================
# DEPARTAMENTOS
# =============================================================================

@router.get("/departamentos", response_model=list[DepartamentoResponse], tags=["Departamentos"])
def listar_departamentos(db: Session = Depends(get_db)):
    """Lista todos os departamentos/unidades acadêmicas cadastrados."""
    return db.query(Departamento).order_by(Departamento.nome).all()


@router.get("/departamentos/{depto_id}/disciplinas", response_model=dict, tags=["Departamentos"])
def disciplinas_por_departamento(
    depto_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """Lista todas as disciplinas de um departamento específico com seus professores."""
    departamento = db.query(Departamento).filter_by(id=depto_id).first()
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")

    query = db.query(Disciplina).filter_by(departamento_id=depto_id)
    total = query.count()
    pages = math.ceil(total / per_page) if total > 0 else 1

    disciplinas = (
        query.order_by(Disciplina.codigo)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return {
        "departamento": DepartamentoResponse.model_validate(departamento),
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
        "items": [DisciplinaResponse.model_validate(d) for d in disciplinas],
    }


@router.get("/departamentos/{depto_id}/professores", response_model=dict, tags=["Departamentos"])
def professores_por_departamento(
    depto_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """Lista todos os professores de um departamento específico."""
    departamento = db.query(Departamento).filter_by(id=depto_id).first()
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")

    query = db.query(Professor).filter_by(departamento_id=depto_id)
    total = query.count()
    pages = math.ceil(total / per_page) if total > 0 else 1

    professores = (
        query.order_by(Professor.nome)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return {
        "departamento": DepartamentoResponse.model_validate(departamento),
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
        "items": [ProfessorResponse.model_validate(p) for p in professores],
    }


@router.post("/departamentos/sincronizar", tags=["Departamentos"])
def sync_departamentos(db: Session = Depends(get_db)):
    """Sincroniza a lista de departamentos do SIGAA no banco de dados."""
    count = sincronizar_departamentos(db)
    return {"message": f"{count} departamentos sincronizados", "total": count}


# =============================================================================
# SCRAPING & ESTATÍSTICAS
# =============================================================================

@router.post("/scraping/iniciar", response_model=ScrapingStatusResponse, tags=["Scraping"])
async def iniciar_scraping(
    background_tasks: BackgroundTasks,
    request: ScrapingRequest = ScrapingRequest(),
    db: Session = Depends(get_db),
):
    """
    Inicia o processo de scraping no SIGAA em segundo plano (Background Task).

    Parâmetros:
    - **nivel**: G (Graduação), S (Stricto Sensu), L (Lato Sensu), etc.
    - **departamento_sigaa_id**: ID SIGAA do departamento (ex: 673 para FGA, 508 para CIC, ou null para todos)
    - **tipo**: 2 para Disciplina
    - **buscar_professores**: Se True, também extrai turmas e professores
    - **ano**: Ano letivo (ex: '2026')
    - **periodo**: Período letivo (ex: '2')
    """
    log = ScrapingLog(
        departamento_sigaa_id=request.departamento_sigaa_id,
        nivel=request.nivel,
        status="RUNNING",
        mensagem="Scraping enfileirado para execução em segundo plano",
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    background_tasks.add_task(
        _executar_scraping_background,
        log_id=log.id,
        nivel=request.nivel,
        tipo=request.tipo or 2,
        departamento_sigaa_id=request.departamento_sigaa_id,
        buscar_professores=request.buscar_professores,
        ano=request.ano,
        periodo=request.periodo,
    )

    return {
        "status": "RUNNING",
        "message": "Scraping iniciado em segundo plano com sucesso",
        "log": ScrapingLogResponse.model_validate(log),
    }


@router.get("/scraping/logs", response_model=list[ScrapingLogResponse], tags=["Scraping"])
def listar_logs_scraping(
    limit: int = Query(20, ge=1, le=100, description="Quantidade de logs"),
    db: Session = Depends(get_db),
):
    """Lista o histórico das execuções de scraping."""
    return (
        db.query(ScrapingLog)
        .order_by(ScrapingLog.id.desc())
        .limit(limit)
        .all()
    )


@router.get("/scraping/status/{log_id}", response_model=ScrapingLogResponse, tags=["Scraping"])
def obter_status_log(log_id: int, db: Session = Depends(get_db)):
    """Obtém o status de uma execução específica de scraping pelo ID do log."""
    log = db.query(ScrapingLog).filter_by(id=log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log de scraping não encontrado")
    return log


@router.get("/estatisticas", response_model=EstatisticasResponse, tags=["Estatísticas"])
def obter_estatisticas(db: Session = Depends(get_db)):
    """Retorna estatísticas gerais do banco de dados (disciplinas, departamentos, professores, turmas)."""
    total_disciplinas = db.query(func.count(Disciplina.id)).scalar() or 0
    total_departamentos = db.query(func.count(Departamento.id)).scalar() or 0
    total_professores = db.query(func.count(Professor.id)).scalar() or 0
    total_turmas = db.query(func.count(Turma.id)).scalar() or 0

    niveis_query = (
        db.query(Disciplina.nivel, func.count(Disciplina.id))
        .group_by(Disciplina.nivel)
        .all()
    )
    disciplinas_por_nivel = {nivel: count for nivel, count in niveis_query if nivel}

    ultimo_log = (
        db.query(ScrapingLog)
        .order_by(ScrapingLog.id.desc())
        .first()
    )

    return {
        "total_disciplinas": total_disciplinas,
        "total_departamentos": total_departamentos,
        "total_professores": total_professores,
        "total_turmas": total_turmas,
        "disciplinas_por_nivel": disciplinas_por_nivel,
        "ultimo_scraping": ScrapingLogResponse.model_validate(ultimo_log) if ultimo_log else None,
    }
