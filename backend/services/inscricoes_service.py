"""
Assinatura temporária dos dados acadêmicos já validados pelo histórico.
"""

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from backend.config import get_settings

TEMPO_MAXIMO_TOKEN_SEGUNDOS = 15 * 60
TOKEN_SALT = "monitoraunb-validacao-historico"
SEGREDO_LOCAL_DESENVOLVIMENTO = "dev-insecure-session-secret"


def _serializador() -> URLSafeTimedSerializer:
    settings = get_settings()
    segredo = settings.SESSION_SECRET or SEGREDO_LOCAL_DESENVOLVIMENTO
    return URLSafeTimedSerializer(segredo, salt=TOKEN_SALT)


def gerar_token_validacao(dados: dict) -> str:
    """Assina os dados extraídos para que o frontend não possa alterá-los."""
    return _serializador().dumps(dados)


def ler_token_validacao(token: str) -> dict:
    """Valida a assinatura e a validade temporal do token recebido."""
    try:
        dados = _serializador().loads(
            token,
            max_age=TEMPO_MAXIMO_TOKEN_SEGUNDOS,
        )
    except SignatureExpired as erro:
        raise ValueError(
            "A validação do histórico expirou. Envie o histórico novamente."
        ) from erro
    except BadSignature as erro:
        raise ValueError(
            "O token de validação é inválido. Envie o histórico novamente."
        ) from erro

    if not isinstance(dados, dict):
        raise ValueError("O conteúdo do token de validação é inválido.")

    return dados
