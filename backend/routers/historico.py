from fastapi import APIRouter, UploadFile, Form, File, HTTPException 
from backend.services.historico.leiturapdf import processar_historico
from backend.services.historico.leitura_creditos import ler_tabela, buscar_disciplinas


router = APIRouter()

@router.post("/api/historico")
def receber_historico(arquivo: UploadFile = File(...),
                      disciplina: str = Form(...)
                      ):

    # print(disciplina)

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
        or resultado["status"] is None
    ):
        raise HTTPException(
            status_code=422,
            detail="O arquivo PDF enviado não é um histórico válido."
        )



    """Campo de códigos de teste"""
    arquivo.file.seek(0)
    
    tabela = ler_tabela(arquivo.file)
    tentativas = buscar_disciplinas(tabela, disciplina)

    if not tentativas:
        raise HTTPException(
            status_code=422,
            detail="A disciplina selecionada não foi encontrada."
        )

    print(tentativas)

    return resultado