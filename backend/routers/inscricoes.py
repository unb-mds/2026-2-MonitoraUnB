from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError

from backend.schemas.inscricoes import (
    DadosHistoricoAssinados,
    InscricaoRequest,
    InscricaoResponse,
)
from backend.services.inscricoes_service import ler_token_validacao

router = APIRouter(
    prefix="/inscricoes",
    tags=["Inscricoes"],
)


@router.post("", response_model=InscricaoResponse)
def criar_inscricao(dados: InscricaoRequest) -> InscricaoResponse:
    try:
        dados_assinados = ler_token_validacao(dados.token_validacao)
        historico = DadosHistoricoAssinados.model_validate(dados_assinados)
    except (ValueError, ValidationError) as erro:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(erro),
        ) from erro

    return InscricaoResponse(
        status="validada",
        mensagem=(
            "Os dados da inscrição foram validados."
        ),
        coeficiente_candidatura=historico.coeficiente_candidatura,
    )
