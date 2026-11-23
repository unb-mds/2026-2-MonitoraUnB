"""
Orquestra o scraping do SIGAA e persiste os dados obtidos.
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from backend.config import get_settings
from backend.database.models import (
    Departamento,
    Disciplina,
    Professor,
    ScrapingLog,
    Turma,
)
from backend.scraping.sigaa import DEPARTAMENTOS, NIVEIS, SigaaScraper

logger = logging.getLogger(__name__)
settings = get_settings()

def sincronizar_departamentos(db: Session) -> int:
    """
    Sincroniza a lista de departamentos do SIGAA no banco de dados.
    """
    count = 0
    for sigaa_id, nome in DEPARTAMENTOS.items():
        existing = db.query(Departamento).filter_by(sigaa_id=sigaa_id).first()
        if existing:
            if existing.nome != nome:
                existing.nome = nome
                count += 1
        else:
            db.add(Departamento(sigaa_id=sigaa_id, nome=nome))
            count += 1

    db.commit()
    logger.info(f"Departamentos sincronizados: {count} novos/atualizados")
    return count


def _salvar_disciplina(
    db: Session, disc_data: dict, departamento: Optional[Departamento]
) -> tuple[int, int]:
    """
    Salva ou atualiza uma disciplina no banco de dados.
    """
    existing = (
        db.query(Disciplina)
        .filter_by(codigo=disc_data["codigo"])
        .first()
    )

    if existing:
        changed = False
        if existing.nome != disc_data["nome"]:
            existing.nome = disc_data["nome"]
            changed = True
        if disc_data.get("tipo") and existing.tipo != disc_data["tipo"]:
            existing.tipo = disc_data["tipo"]
            changed = True
        if disc_data.get("carga_horaria") and existing.carga_horaria != disc_data["carga_horaria"]:
            existing.carga_horaria = disc_data["carga_horaria"]
            changed = True
        if departamento and existing.departamento_id != departamento.id:
            existing.departamento_id = departamento.id
            changed = True
        return (0, 1 if changed else 0)
    else:
        nova = Disciplina(
            codigo=disc_data["codigo"],
            nome=disc_data["nome"],
            tipo=disc_data.get("tipo"),
            nivel=disc_data.get("nivel"),
            carga_horaria=disc_data.get("carga_horaria"),
            departamento_id=departamento.id if departamento else None,
        )
        db.add(nova)
        return (1, 0)


def _salvar_professores_e_turmas(
    db: Session,
    disc_turmas: list[dict],
    departamento: Optional[Departamento],
    nivel: str,
) -> tuple[int, int]:
    """
    Salva ou atualiza professores, turmas e seus relacionamentos com disciplinas.
    Retorna (total_professores_novos, total_turmas_novas).
    """
    professores_novos = 0
    turmas_novas = 0
    nivel_str = NIVEIS.get(nivel, nivel)

    for item in disc_turmas:
        # 1. Localizar ou criar a disciplina
        disciplina = (
            db.query(Disciplina)
            .filter_by(codigo=item["codigo"], nivel=nivel_str)
            .first()
        )
        if not disciplina:
            disciplina = db.query(Disciplina).filter_by(codigo=item["codigo"]).first()

        if not disciplina:
            disciplina = Disciplina(
                codigo=item["codigo"],
                nome=item["nome"],
                tipo="DISCIPLINA",
                nivel=nivel_str,
                departamento_id=departamento.id if departamento else None,
            )
            db.add(disciplina)
            db.flush()
        else:
            if departamento and not disciplina.departamento_id:
                disciplina.departamento_id = departamento.id

        # 2. Salvar professores e associar à disciplina
        professores_map = {}
        for prof_nome in item["professores"]:
            prof = db.query(Professor).filter_by(nome=prof_nome).first()
            if not prof:
                prof = Professor(
                    nome=prof_nome,
                    departamento_id=departamento.id if departamento else None,
                )
                db.add(prof)
                db.flush()
                professores_novos += 1
            elif departamento and not prof.departamento_id:
                prof.departamento_id = departamento.id

            professores_map[prof_nome] = prof

            if prof not in disciplina.professores:
                disciplina.professores.append(prof)

        # 3. Salvar turmas e associar professores
        for t_data in item["turmas"]:
            turma = (
                db.query(Turma)
                .filter_by(
                    disciplina_id=disciplina.id,
                    codigo=t_data["codigo"],
                    ano_periodo=t_data["ano_periodo"],
                )
                .first()
            )
            if not turma:
                turma = Turma(
                    disciplina_id=disciplina.id,
                    codigo=t_data["codigo"],
                    ano_periodo=t_data["ano_periodo"],
                    horario=t_data["horario"],
                    local=t_data["local"],
                    vagas_ofertadas=t_data["vagas_ofertadas"],
                    vagas_ocupadas=t_data["vagas_ocupadas"],
                )
                db.add(turma)
                db.flush()
                turmas_novas += 1
            else:
                turma.horario = t_data["horario"]
                turma.local = t_data["local"]
                turma.vagas_ofertadas = t_data["vagas_ofertadas"]
                turma.vagas_ocupadas = t_data["vagas_ocupadas"]

            # Associar professores da turma específica
            for doc_nome in t_data["docentes"]:
                doc_obj = professores_map.get(doc_nome)
                if not doc_obj:
                    doc_obj = db.query(Professor).filter_by(nome=doc_nome).first()
                if doc_obj and doc_obj not in turma.professores:
                    turma.professores.append(doc_obj)

    return professores_novos, turmas_novas


async def executar_scraping(
    db: Session,
    log_id: Optional[int] = None,
    nivel: str = "G",
    tipo: int = 2,
    departamento_sigaa_id: Optional[int] = None,
    buscar_professores: bool = True,
    ano: Optional[str] = None,
    periodo: Optional[str] = None,
) -> ScrapingLog:
    """
    Executa o scraping e salva disciplinas, turmas e professores no banco de dados.
    """
    if log_id:
        log = db.query(ScrapingLog).filter_by(id=log_id).first()
        if not log:
            log = ScrapingLog(
                departamento_sigaa_id=departamento_sigaa_id,
                nivel=NIVEIS.get(nivel, nivel),
                status="RUNNING",
            )
            db.add(log)
    else:
        log = ScrapingLog(
            departamento_sigaa_id=departamento_sigaa_id,
            nivel=NIVEIS.get(nivel, nivel),
            status="RUNNING",
        )
        db.add(log)
    db.commit()

    scraper = SigaaScraper()
    total_encontradas = 0
    total_novas = 0
    total_atualizadas = 0
    total_professores = 0
    total_turmas = 0

    try:
        sincronizar_departamentos(db)

        if departamento_sigaa_id:
            deptos = [departamento_sigaa_id]
        else:
            deptos = list(DEPARTAMENTOS.keys())

        for depto_id in deptos:
            try:
                logger.info(
                    f"Scraping departamento {depto_id}: {DEPARTAMENTOS.get(depto_id, 'Desconhecido')}"
                )
                depto_db = db.query(Departamento).filter_by(sigaa_id=depto_id).first()

                # 1. Buscar catálogo de componentes
                disciplinas = await scraper.buscar_componentes(
                    nivel=nivel,
                    tipo=tipo,
                    unidade_id=depto_id,
                )

                for disc_data in disciplinas:
                    total_encontradas += 1
                    novas, atualizadas = _salvar_disciplina(db, disc_data, depto_db)
                    total_novas += novas
                    total_atualizadas += atualizadas

                db.commit()

                # 2. Se habilitado, buscar turmas e professores
                if buscar_professores:
                    await asyncio.sleep(settings.SCRAPER_DELAY)
                    disc_turmas = await scraper.buscar_turmas(
                        nivel=nivel,
                        unidade_id=depto_id,
                        ano=ano,
                        periodo=periodo,
                    )
                    novos_profs, novas_turmas = _salvar_professores_e_turmas(
                        db=db,
                        disc_turmas=disc_turmas,
                        departamento=depto_db,
                        nivel=nivel,
                    )
                    total_professores += novos_profs
                    total_turmas += novas_turmas
                    db.commit()

                await asyncio.sleep(settings.SCRAPER_DELAY)

            except Exception as e:
                logger.error(f"Erro no departamento {depto_id}: {e}")
                continue

        log.status = "SUCCESS"
        log.disciplinas_encontradas = total_encontradas
        log.disciplinas_novas = total_novas
        log.disciplinas_atualizadas = total_atualizadas
        log.professores_encontrados = total_professores
        log.turmas_encontradas = total_turmas
        log.mensagem = (
            f"Scraping concluído: {total_encontradas} disciplinas catalogadas "
            f"({total_novas} novas, {total_atualizadas} atualizadas), "
            f"{total_professores} novos professores, {total_turmas} novas turmas."
        )
        log.finished_at = datetime.utcnow()

    except Exception as e:
        logger.error(f"Erro durante o scraping: {e}")
        log.status = "ERROR"
        log.mensagem = str(e)[:500]
        log.finished_at = datetime.utcnow()

    finally:
        await scraper.close()
        db.commit()

    return log
