"""
API para extração de Scraping do SIGAA da
Universidade de Brasília (UnB).
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="SIGAA UnB - API de Disciplinas e Professores",
    description="""
API para extração e consulta de disciplinas, turmas e professores do SIGAA UnB.
Fontes públicas utilizadas:
- Componentes curriculares: `https://sigaa.unb.br/sigaa/public/componentes/busca_componentes.jsf`
- Turmas e Docentes: `https://sigaa.unb.br/sigaa/public/turmas/listar.jsf`
    """,
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")
