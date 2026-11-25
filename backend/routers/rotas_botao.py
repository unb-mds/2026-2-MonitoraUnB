"""
Rotas administrativas para criação e gestão de processos seletivos.

Todas as rotas exigem professor/administrador autenticado via sessão
(`Depends(require_professor)`).
"""
from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from backend.config import get_settings
from backend.database.database import get_db
from backend.database.models import ProcessoSeletivo, UsuarioAdministrador
from backend.dependencies.auth import require_professor

router = APIRouter(prefix="/admin/processos", tags=["admin"])


class NovoProcesso(BaseModel):
    semestre: str = Field(pattern=r"^\d{4}/[12]$")
    data_abertura: date
    data_encerramento: date


def _obter_id_usuario_admin(db: Session, username: str) -> int:
    """Retorna o id_usuario responsável na tabela usuario_administrador."""
    email_padrao = f"{username}@unb.br" if "@" not in username else username

    admin = (
        db.query(UsuarioAdministrador)
        .filter(
            UsuarioAdministrador.email == email_padrao,
            UsuarioAdministrador.ativo.is_(True),
        )
        .first()
    )
    if admin is None:
        admin = (
            db.query(UsuarioAdministrador)
            .filter(UsuarioAdministrador.ativo.is_(True))
            .order_by(UsuarioAdministrador.id_usuario.asc())
            .first()
        )
    if admin is not None:
        return int(admin.id_usuario)

    settings = get_settings()
    senha_hash = (settings.PROFESSOR_PASSWORD_HASH or "hash_provisorio").replace("$$", "$")
    novo_admin = UsuarioAdministrador(
        email=email_padrao,
        senha_hash=senha_hash,
        ativo=True,
    )
    try:
        db.add(novo_admin)
        db.commit()
        db.refresh(novo_admin)
        return int(novo_admin.id_usuario)
    except DBAPIError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Nenhum usuário administrador ativo encontrado no banco de dados.",
        ) from e


def _executar(db: Session, sql: str, params: dict, *, scalar_one: bool = False):
    """Executa o SQL, consome o resultado quando necessário e traduz erros do banco."""
    try:
        resultado = db.execute(text(sql), params)
        valor = resultado.scalar_one() if scalar_one else resultado.rowcount
        db.commit()
        return valor
    except DBAPIError as e:
        db.rollback()
        bruto = str(getattr(e, "orig", e))
        if "uq_processo_aberto" in bruto:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um processo aberto. Encerre-o antes de abrir outro.",
            ) from e
        if "uq_processo_seletivo" in bruto:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um processo seletivo cadastrado para este semestre.",
            ) from e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=bruto.strip().splitlines()[0],
        ) from e


@router.get("")
def listar(
    db: Session = Depends(get_db),
    _professor: str = Depends(require_professor),
):
    linhas = db.execute(
        text(
            "SELECT id_processo, semestre, data_abertura, data_encerramento, status "
            "FROM processo_seletivo ORDER BY data_abertura DESC, id_processo DESC"
        )
    ).mappings().all()
    return [{"id": l["id_processo"], **dict(l)} for l in linhas]


@router.post("", status_code=status.HTTP_201_CREATED)
def criar(
    dados: NovoProcesso,
    db: Session = Depends(get_db),
    professor: str = Depends(require_professor),
):
    if dados.data_encerramento < dados.data_abertura:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A data de fim das inscrições não pode ser anterior à data de início.",
        )

    existente = (
        db.query(ProcessoSeletivo)
        .filter(ProcessoSeletivo.semestre == dados.semestre)
        .first()
    )
    if existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe um processo seletivo cadastrado para o semestre {dados.semestre}.",
        )

    id_usuario = _obter_id_usuario_admin(db, professor)
    id_processo = _executar(
        db,
        "INSERT INTO processo_seletivo (id_usuario, semestre, data_abertura, data_encerramento) "
        "VALUES (:u, :s, :a, :e) RETURNING id_processo",
        {
            "u": id_usuario,
            "s": dados.semestre,
            "a": dados.data_abertura,
            "e": dados.data_encerramento,
        },
        scalar_one=True,
    )
    return {
        "id": id_processo,
        "id_processo": id_processo,
        "semestre": dados.semestre,
        "data_abertura": dados.data_abertura.isoformat(),
        "data_encerramento": dados.data_encerramento.isoformat(),
        "status": "AGENDADO",
    }


def _mudar_status(db: Session, id_processo: int, novo: str):
    if novo == "ABERTO":
        outro_aberto = (
            db.query(ProcessoSeletivo)
            .filter(
                ProcessoSeletivo.status == "ABERTO",
                ProcessoSeletivo.id_processo != id_processo,
            )
            .first()
        )
        if outro_aberto is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um processo aberto. Encerre-o antes de abrir outro.",
            )

    linhas_afetadas = _executar(
        db,
        "UPDATE processo_seletivo SET status = :s WHERE id_processo = :i",
        {"s": novo, "i": id_processo},
    )
    if linhas_afetadas == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Processo não encontrado.",
        )
    return {"ok": True}


@router.post("/{id_processo}/abrir")
def abrir(
    id_processo: int,
    db: Session = Depends(get_db),
    _professor: str = Depends(require_professor),
):
    return _mudar_status(db, id_processo, "ABERTO")


@router.post("/{id_processo}/encerrar")
def encerrar(
    id_processo: int,
    db: Session = Depends(get_db),
    _professor: str = Depends(require_professor),
):
    return _mudar_status(db, id_processo, "ENCERRADO")


@router.post("/{id_processo}/limpar")
def limpar(
    id_processo: int,
    db: Session = Depends(get_db),
    _professor: str = Depends(require_professor),
):
    _executar(db, "SELECT limpar_processo_encerrado(:i)", {"i": id_processo})
    return {"ok": True}
