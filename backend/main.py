from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

'''o CORS está sendo usado para permitir a comunicação da API com o frontend, pois ambos utilizavam portas diferentes'''

from backend.routers import (
    disciplinas,
    historico,
    inscricoes
)


app = FastAPI()

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

@app.get("/")
def raiz():
    return{
        "mensagem": "API MonitoraUnB funcionando"
    }


