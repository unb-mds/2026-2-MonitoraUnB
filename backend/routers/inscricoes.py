import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.schemas.inscricoes import (
    DadosHistoricoAssinados,
    InscricaoRequest,
    InscricaoResponse,
)
from backend.services.inscricoes_service import (
    DisciplinaNaoEncontradaError,
    InscricaoDuplicadaError,
    ProcessoNaoAbertoError,
    ProcessoNaoEncontradoError,
    ler_token_validacao,
    registrar_inscricao,
)

router = APIRouter(
    prefix="/inscricoes",
    tags=["Inscricoes"],
)

logger = logging.getLogger(__name__)


@router.post("", response_model=InscricaoResponse)
def criar_inscricao(
    dados: InscricaoRequest,
    db: Session = Depends(get_db),
) -> InscricaoResponse:
    try:
        dados_assinados = ler_token_validacao(dados.token_validacao)
        historico = DadosHistoricoAssinados.model_validate(dados_assinados)
    except (ValueError, ValidationError) as erro:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(erro),
        ) from erro

    if historico.status.strip().upper() != "ATIVO":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Somente estudantes com status acadêmico ATIVO podem se inscrever.",
        )

    if historico.disciplina.situacao.strip().upper() != "APROVADO":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A disciplina precisa estar aprovada no histórico do estudante.",
        )

    try:
        registrar_inscricao(
            db=db,
            historico=historico,
            semestre=dados.semestre,
            email=dados.email,
        )
    except DisciplinaNaoEncontradaError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="A disciplina ainda não está cadastrada no sistema.",
        ) from erro
    except ProcessoNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não existe processo seletivo cadastrado para o semestre informado.",
        ) from erro
    except ProcessoNaoAbertoError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="O processo seletivo informado não está aberto para inscrições.",
        ) from erro
    except InscricaoDuplicadaError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="O estudante já possui uma inscrição neste processo seletivo.",
        ) from erro
    except SQLAlchemyError as erro:
        db.rollback()
        logger.exception("Erro ao gravar inscrição no banco de dados.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível gravar a inscrição no banco de dados.",
        ) from erro

    return InscricaoResponse(
        status="registrada",
        mensagem="Inscrição registrada com sucesso.",
        coeficiente_candidatura=historico.coeficiente_candidatura,
    )
