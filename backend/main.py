from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
'''o CORS está sendo usado para permitir a comunicação da API com o frontend, pois ambos utilizavam portas diferentes'''

import logging


from backend.routers import (
    disciplinas,
    historico,
    inscricoes,
    departamentos
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

@app.get("/")
def raiz():
    return{
        "mensagem": "API MonitoraUnB funcionando"
    }


