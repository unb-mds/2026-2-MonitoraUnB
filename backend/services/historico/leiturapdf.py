import re
from pypdf import PdfReader
from pypdf.generic import NullObject
from pathlib import Path


def ler_status(texto):  
    '''O aluno precisa obrigatoriamente estar com o status como ativo para poder se matricular.'''
    status_local = re.search(
            r"\b(ATIVO|FORMANDO|TRANCADO|CADASTRADO|CANCELADO|DESLIGADO)\b",
            texto,
            re.IGNORECASE
            )

    if status_local:
        status = status_local.group(1).strip().upper()
        return status

    return None

def ler_pdf(arquivo):
    historico = PdfReader(arquivo)
    texto = historico.pages[0].extract_text(extraction_mode="layout")
    return texto

def ler_ira(texto):
    ira_local = re.search(r"\bIRA:\s*(\d+(?:[.,]\d+)?)", texto)
    if ira_local:
        ira = float(ira_local.group(1).replace(",", "."))
        return ira
    else:
        return None

def ler_nome(texto):
    nome_local = re.search(r"\bNome:\s*(.+?)\s+Matrícula", texto)
    if nome_local:
        nome = nome_local.group(1).strip()
        return nome
    else:
        return None

def ler_matricula(texto):
    matricula_local = re.search(r"\bMatrícula:\s*(\d+)?", texto)
    if matricula_local:
        matricula = matricula_local.group(1)
        return matricula
    else:
        return None

def processar_historico(arquivo):
    texto = ler_pdf(arquivo)

    status = ler_status(texto)
    nome = ler_nome(texto)
    matricula = ler_matricula(texto)
    ira = ler_ira(texto)

    return {
        "aluno": nome,
        "matricula": matricula,
        "ira": ira,
        "status": status
    }
