from fastapi import APIRouter, UploadFile, Form, File, HTTPException 
from pypdf.errors import PyPdfError
import re

from backend.services.historico.leiturapdf import processar_historico
from backend.services.historico.leitura_creditos import (
    ler_tabela, 
    buscar_disciplinas, 
    buscar_mencao,
)
from backend.services.historico.calcular_coeficiente import calcular_coeficiente
from backend.services.inscricoes_service import gerar_token_validacao


router = APIRouter()


@router.post("/historico")
def receber_historico(arquivo: UploadFile = File(...),
                      disciplina: str = Form(...),
                      matricula: str = Form(...),
                      ):


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
    try:
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

        matricula_pdf = re.sub(r"\D", "", resultado["matricula"])
        matricula_informada = re.sub(r"\D", "", matricula)
        if not matricula_informada or matricula_informada != matricula_pdf:
            raise HTTPException(
                status_code=422,
                detail="A matrícula informada não corresponde à matrícula do histórico.",
            )

        arquivo.file.seek(0)
        tabela = ler_tabela(arquivo.file)
        tentativas = buscar_disciplinas(tabela, disciplina)

    except (PyPdfError, ValueError, IndexError) as erro:
        raise HTTPException(
            status_code=422,
            detail="Não foi possível interpretar o PDF como um histórico válido.",
        ) from erro

    if not tentativas:
        raise HTTPException(
            status_code=422,
            detail="A disciplina selecionada não foi encontrada."
        )

    def periodo_chave(tentativa):
        ano, semestre = tentativa["periodo"].split(".")
        return int(ano), int(semestre)

    tentativa_mais_recente = max(tentativas, key=periodo_chave)

    if tentativa_mais_recente["sigla"].strip().upper() == "MATR":
        raise HTTPException(
            status_code=422,
            detail="Não é possível se matricular a uma disciplina que está cursando.",
        )

    try:
        aprovacoes = buscar_mencao(tabela, disciplina)
    except ValueError as erro:
        raise HTTPException(
            status_code=422,
            detail=str(erro)
        ) from erro

    tentativa_considerada = aprovacoes["mais_recente"]

    try:
        coeficiente_candidatura = calcular_coeficiente(
            resultado["ira"],
            tentativa_considerada["coef_mencao"],
        )
    except ValueError as erro:
        raise HTTPException(status_code=422, detail=str(erro)) from erro

    dados_validados = {
        **resultado,
        "disciplina": {
            "codigo": tentativa_considerada["codigo"],
            "nome": tentativa_considerada["disciplina"],
            "mencao": tentativa_considerada["mencao"],
            "situacao": tentativa_considerada["situacao"],
            "periodo": tentativa_considerada["periodo"],
            "coef_mencao": tentativa_considerada["coef_mencao"],
        },
        "coeficiente_candidatura": coeficiente_candidatura,
    }

    return {
        **dados_validados,
        "token_validacao": gerar_token_validacao(dados_validados),
    }
