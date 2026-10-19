"""
Rotas da API REST para consulta e gerenciamento das disciplinas do SIGAA UnB.
"""

import math
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Departamento, Disciplina, ScrapingLog
from app.schemas import (
    DepartamentoResponse,
    DisciplinaResponse,
    DisciplinaComDepartamento,
    ScrapingRequest,
    ScrapingLogResponse,
    ScrapingStatusResponse,
    EstatisticasResponse,
)
from app.scraper import executar_scraping, sincronizar_departamentos

logger = logging.getLogger(__name__)

router = APIRouter()

# DISCIPLINAS

@router.get("/disciplinas", response_model=dict, tags=["Disciplinas"])
def listar_disciplinas(
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(50, ge=1, le=200, description="Itens por página"),
    codigo: Optional[str] = Query(None, description="Filtrar por código (busca parcial)"),
    nome: Optional[str] = Query(None, description="Filtrar por nome (busca parcial)"),
    nivel: Optional[str] = Query(None, description="Filtrar por nível de ensino"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo"),
    departamento_id: Optional[int] = Query(None, description="Filtrar por ID do departamento"),
    db: Session = Depends(get_db),
):
    """
    Lista disciplinas com paginação e filtros opcionais.

    Suporta busca parcial por código e nome (LIKE '%valor%').
    """
    query = db.query(Disciplina)

    # Aplicar filtros
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

    # Contagem
    total = query.count()
    pages = math.ceil(total / per_page) if total > 0 else 1

    disciplinas = (
        query.order_by(Disciplina.codigo)
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
def buscar_por_codigo(codigo: str, db: Session = Depends(get_db)):
    """Busca disciplinas pelo código exato ou parcial."""
    disciplinas = (
        db.query(Disciplina)
        .filter(Disciplina.codigo.ilike(f"%{codigo}%"))
        .order_by(Disciplina.codigo)
        .all()
    )
    if not disciplinas:
        raise HTTPException(status_code=404, detail="Nenhuma disciplina encontrada com esse código")
    return disciplinas

# DEPARTAMENTOS
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
    """Lista todas as disciplinas de um departamento específico."""
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


@router.post("/departamentos/sincronizar", tags=["Departamentos"])
def sync_departamentos(db: Session = Depends(get_db)):
    """Sincroniza a lista de departamentos do SIGAA no banco de dados."""
    count = sincronizar_departamentos(db)
    return {"message": f"{count} departamentos sincronizados", "total": count}
