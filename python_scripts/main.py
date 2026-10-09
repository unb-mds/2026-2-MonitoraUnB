from leiturapdf import processar_historico
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# o CORS está sendo usado para permitir a comunicação da API com o frontend, pois ambos utilizavam portas diferentes

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


@app.get("/")
def raiz():
    return{
        "mensagem": "API MonitoraUnB funcionando"
    }


@app.post("/api/historico")
def receber_historico(arquivo: UploadFile = File(...)):

    if (arquivo.content_type != "application/pdf"):
        raise HTTPException(
            status_code=400,
            detail="O arquivo enviado deve ser um PDF."
        )

    if not (arquivo.filename or "").lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="O arquivo enviado deve possuir a extensão PDF."
        )

    resultado = processar_historico(arquivo.file)

    if (
        resultado["aluno"] is None
        or resultado["matricula"] is None
        or resultado["ira"] is None
    ):
        raise HTTPException(
            status_code=422,
            detail="O arquivo PDF enviado não é um histórico válido."
        )

    return resultado
# resultado = processar_historico(r"C:\Users\Marcelo\Downloads\historico_251022427.pdf")
# print(f"{resultado}")


