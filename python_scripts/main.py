from leiturapdf import processar_historico
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()


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


