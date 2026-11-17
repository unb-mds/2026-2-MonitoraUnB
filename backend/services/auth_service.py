"""
Serviço de autenticação do professor (credencial única + hash bcrypt).
"""

from __future__ import annotations

from passlib.context import CryptContext

from backend.config import Settings, get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SESSION_FLAG = "professor_authenticated"
SESSION_USERNAME = "professor_username"


def verificar_credenciais(
    username: str,
    password: str,
    settings: Settings | None = None,
) -> bool:
    """Retorna True se username/senha batem com a credencial configurada no .env."""
    settings = settings or get_settings()

    if not settings.PROFESSOR_USERNAME or not settings.PROFESSOR_PASSWORD_HASH:
        return False

    if username != settings.PROFESSOR_USERNAME:
        return False

    try:
        return pwd_context.verify(password, settings.PROFESSOR_PASSWORD_HASH)
    except (ValueError, TypeError):
        return False


def marcar_sessao_professor(session: dict, username: str) -> None:
    session[SESSION_FLAG] = True
    session[SESSION_USERNAME] = username


def limpar_sessao_professor(session: dict) -> None:
    session.pop(SESSION_FLAG, None)
    session.pop(SESSION_USERNAME, None)


def professor_autenticado(session: dict) -> bool:
    return bool(session.get(SESSION_FLAG))


def username_da_sessao(session: dict) -> str | None:
    if not professor_autenticado(session):
        return None
    username = session.get(SESSION_USERNAME)
    return username if isinstance(username, str) else None
