import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.schemas.inscricoes import (
    DadosHistoricoAssinados,
    InscricaoRequest,
    InscricaoRankingResponse,
    InscricaoResponse,
    ProcessoAbertoResponse,
)
from backend.services.auth_service import professor_autenticado
from backend.services.inscricoes_service import (
    DisciplinaNaoEncontradaError,
    InscricaoDuplicadaError,
    ProcessoNaoAbertoError,
    ProcessoNaoEncontradoError,
    gerar_planilha_inscricoes,
    ler_token_validacao,
    listar_inscricoes as listar_inscricoes_service,
    obter_processo_aberto as obter_processo_aberto_service,
    registrar_inscricao,
)

router = APIRouter(
    prefix="/inscricoes",
    tags=["Inscricoes"],
)

logger = logging.getLogger(__name__)


@router.get("/processo-aberto", response_model=ProcessoAbertoResponse)
def consultar_processo_aberto(
    db: Session = Depends(get_db),
) -> ProcessoAbertoResponse:
    try:
        processo = obter_processo_aberto_service(db)
    except SQLAlchemyError as erro:
        db.rollback()
        logger.exception("Erro ao consultar o processo seletivo aberto.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível consultar o processo seletivo no banco de dados.",
        ) from erro

    if processo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há processo seletivo aberto para inscrições.",
        )

    return ProcessoAbertoResponse(semestre=processo.semestre)


@router.get("", response_model=list[InscricaoRankingResponse])
def obter_inscricoes(
    request: Request,
    semestre: str = Query(..., pattern=r"^\d{4}/[12]$"),
    db: Session = Depends(get_db),
) -> list[dict]:
    if not professor_autenticado(request.session):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="É necessário autenticar como professor para consultar inscrições.",
        )

    try:
        return listar_inscricoes_service(db=db, semestre=semestre)
    except ProcessoNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não existe processo seletivo cadastrado para o semestre informado.",
        ) from erro
    except SQLAlchemyError as erro:
        db.rollback()
        logger.exception("Erro ao consultar inscrições no banco de dados.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível consultar as inscrições no banco de dados.",
        ) from erro


@router.get("/planilha")
def baixar_planilha_inscricoes(
    request: Request,
    semestre: str = Query(..., pattern=r"^\d{4}/[12]$"),
    disciplina: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> Response:
    if not professor_autenticado(request.session):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="É necessário autenticar como professor para baixar a planilha.",
        )

    try:
        conteudo = gerar_planilha_inscricoes(
            db=db,
            semestre=semestre,
            disciplina=disciplina,
        )
    except ProcessoNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não existe processo seletivo cadastrado para o semestre informado.",
        ) from erro
    except SQLAlchemyError as erro:
        db.rollback()
        logger.exception("Erro ao gerar planilha de inscrições.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível gerar a planilha de inscrições.",
        ) from erro

    nome_arquivo = f"inscricoes-monitoria-{semestre.replace('/', '-')}.xlsx"
    return Response(
        content=conteudo,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="{nome_arquivo}"',
        },
    )


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
