"""
Rotas do painel do administrador (exemplo em FastAPI).

COMO ENCAIXAR NO PROJETO:
  1) Ajuste os 2 imports marcados com TODO para os do projeto.
  2) No arquivo principal:  app.include_router(router)
  3) Rode o backend com o usuário do banco `monitora_app`.

Todas as rotas exigem administrador logado (Depends(obter_admin_logado)).
O banco já impõe as regras (um processo aberto por vez, só abre com disciplinas,
só encerra com tudo decidido/enviado); aqui só traduzimos os erros.
"""
from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from backend.database.session import get_db            # TODO: ajustar ao projeto
from backend.auth import obter_admin_logado             # TODO: ajustar ao projeto

router = APIRouter(prefix="/admin/processos", tags=["admin"])


class NovoProcesso(BaseModel):
    semestre: str = Field(pattern=r"^\d{4}/\d$")
    data_abertura: date
    data_encerramento: date


def _executar(db: Session, sql: str, params: dict):
    """Executa o SQL e traduz erros do banco para mensagens legíveis."""
    try:
        resultado = db.execute(text(sql), params)
        db.commit()
        return resultado
    except DBAPIError as e:
        db.rollback()
        bruto = str(getattr(e, "orig", e))
        if "uq_processo_aberto" in bruto:
            raise HTTPException(409, "Já existe um processo aberto. Encerre-o antes de abrir outro.")
        raise HTTPException(400, bruto.strip().splitlines()[0])


@router.get("")
def listar(db: Session = Depends(get_db), admin=Depends(obter_admin_logado)):
    linhas = db.execute(text(
        "SELECT id_processo, semestre, data_abertura, data_encerramento, status "
        "FROM processo_seletivo ORDER BY data_abertura DESC, id_processo DESC"
    )).mappings().all()
    return [dict(l) for l in linhas]


@router.post("", status_code=201)
def criar(dados: NovoProcesso, db: Session = Depends(get_db), admin=Depends(obter_admin_logado)):
    r = _executar(db,
        "INSERT INTO processo_seletivo (id_usuario, semestre, data_abertura, data_encerramento) "
        "VALUES (:u, :s, :a, :e) RETURNING id_processo",
        {"u": admin.id_usuario, "s": dados.semestre, "a": dados.data_abertura, "e": dados.data_encerramento})
    return {"id_processo": r.scalar_one()}


def _mudar_status(db: Session, id_processo: int, novo: str):
    r = _executar(db, "UPDATE processo_seletivo SET status = :s WHERE id_processo = :i",
                  {"s": novo, "i": id_processo})
    if r.rowcount == 0:
        raise HTTPException(404, "Processo não encontrado.")
    return {"ok": True}


@router.post("/{id_processo}/abrir")
def abrir(id_processo: int, db: Session = Depends(get_db), admin=Depends(obter_admin_logado)):
    return _mudar_status(db, id_processo, "ABERTO")


@router.post("/{id_processo}/encerrar")
def encerrar(id_processo: int, db: Session = Depends(get_db), admin=Depends(obter_admin_logado)):
    return _mudar_status(db, id_processo, "ENCERRADO")


@router.post("/{id_processo}/limpar")
def limpar(id_processo: int, db: Session = Depends(get_db), admin=Depends(obter_admin_logado)):
    _executar(db, "SELECT limpar_processo_encerrado(:i)", {"i": id_processo})
    return {"ok": True}
