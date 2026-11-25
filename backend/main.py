from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
'''o CORS está sendo usado para permitir a comunicação da API com o frontend, pois ambos utilizavam portas diferentes'''

import logging


from backend.config import get_settings
from backend.routers import (
    auth,
    disciplinas,
    historico,
    inscricoes,
    departamentos,
    rotas_botao,
    scraping,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI(
    title="MonitoraUnB API",
    description="API do sistema MonitoraUnB para processamento de históricos, disciplinas e inscrições.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

settings = get_settings()

# add_middleware empilha de dentro para fora: o último adicionado é o mais externo.
# Session primeiro, CORS por último → CORS trata o preflight antes da sessão.
if not settings.SESSION_SECRET:
    logging.getLogger(__name__).warning(
        "SESSION_SECRET vazio no .env — usando valor inseguro só para desenvolvimento local."
    )

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET or "dev-insecure-session-secret",
    session_cookie="monitora_session",
    same_site="lax",
    https_only=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth.router,
    prefix="/api"
)

app.include_router(
    historico.router,
    prefix="/api"
)

app.include_router(
    disciplinas.router,
    prefix="/api"
)

app.include_router(
    inscricoes.router,
    prefix="/api"
)

app.include_router(
    departamentos.router,
    prefix="/api"
)

app.include_router(
    rotas_botao.router,
    prefix="/api"
)

app.include_router(
    scraping.router,
    prefix="/api/v1",
)

@app.get("/")
def raiz():
    return{
        "mensagem": "API MonitoraUnB funcionando"
    }


