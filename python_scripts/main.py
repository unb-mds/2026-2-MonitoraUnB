from leiturapdf import processar_historico
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from leitura_creditos import puxar_tabela, ler_tabela, buscar_mencao
#from leiturapdf import (
# arquivo_pdf,
# ler_status,
# ler_matricula,
# ler_nome,
# ler_ira,
# texto
# )


from calcular_coeficiente import calcular_coeficiente

# from leitura_creditos import gerar_txt

'''o CORS está sendo usado para permitir a comunicação da API com o frontend, pois ambos utilizavam portas diferentes'''

app = FastAPI()

#puxar_tabela(texto)
# tabela = ler_tabela(arquivo_pdf)

# buscar_mencao(tabela, FGA0071, MS)


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
def receber_historico(arquivo: UploadFile = File(...),
                      disciplina: str = Form(...)
                      ):

    print(disciplina)

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

# try:
#     resultado = buscar_mencao(tabela, codigo)

#     coeficiente = calcular_coeficiente(
#         ira,
#         resultado["coef_mencao"]
#         )
# except ValueError as erro:
#     print("DEU ERRO")
#        print(resultado["disciplina"])
#        print(resultado["codigo"])
#        print(resultado["mencao"])
#        print(resultado["coef_mencao"])
#        print(resultado["creditos"])
#        print(resultado["periodo"])
#        print(resultado["situacao"])        tudo aqui foi teste para saber se estava funcionando
#        print(coeficiente)