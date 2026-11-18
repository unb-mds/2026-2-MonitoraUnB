"""Dependências FastAPI para proteger rotas do professor."""

from fastapi import HTTPException, Request, status

from backend.services import auth_service


def require_professor(request: Request) -> str:
    """
    Exige sessão de professor autenticado.
    Retorna o username da sessão ou responde 401.
    """
    username = auth_service.username_da_sessao(request.session)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação de professor necessária.",
        )
    return username
