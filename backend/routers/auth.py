"""Rotas de autenticação do professor."""

from fastapi import APIRouter, HTTPException, Request, status

from backend.config import get_settings
from backend.schemas.auth import (
    LoginRequest,
    LoginResponse,
    MeResponse,
    MensagemResponse,
)
from backend.services import auth_service

router = APIRouter(
    prefix="/auth", 
    tags=["Auth"]
)


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, request: Request) -> LoginResponse:
    settings = get_settings()

    if not settings.PROFESSOR_USERNAME or not settings.PROFESSOR_PASSWORD_HASH:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Credencial do professor não configurada. "
                "Defina PROFESSOR_USERNAME e PROFESSOR_PASSWORD_HASH no .env."
            ),
        )

    if not auth_service.verificar_credenciais(
        body.username,
        body.password,
        settings,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login ou senha inválidos.",
        )

    auth_service.marcar_sessao_professor(request.session, body.username)
    return LoginResponse(
        mensagem="Login realizado com sucesso.",
        username=body.username,
    )


@router.post("/logout", response_model=MensagemResponse)
def logout(request: Request) -> MensagemResponse:
    auth_service.limpar_sessao_professor(request.session)
    return MensagemResponse(mensagem="Logout realizado com sucesso.")


@router.get("/me", response_model=MeResponse)
def me(request: Request) -> MeResponse:
    username = auth_service.username_da_sessao(request.session)
    return MeResponse(
        authenticated=username is not None,
        username=username,
    )
