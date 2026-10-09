from leiturapdf import processar_historico
from fastapi import FastAPI

app = FastAPI


@app.get("/")
def raiz():
    return{
        "mensagem": "API MonitoraUnB funcionando"
    }

# resultado = processar_historico(r"C:\Users\Marcelo\Downloads\historico_251022427.pdf")
# print(f"{resultado}\n\n\n")


