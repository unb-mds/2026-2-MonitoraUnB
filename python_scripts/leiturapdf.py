from logging import NullHandler
import re
from pypdf import PdfReader
from pypdf.generic import NullObject

historico = PdfReader("historico26.2.pdf")

texto = historico.pages[0].extract_text(extraction_mode="layout")

def ler_ira():
    ira_local = re.search(r"\bIRA:\s*(\d+(?:[.,]\d+)?)", texto)
    if ira_local:
#        print(ira_local.group(1)) # teste para saber se peguei o ira
        ira = float(ira_local.group(1))
        return ira
    else:
        print("Documento Invalido") #colocar acentos
        return None

def ler_nome():
    nome_local = re.search(r"\bNome:\s*(.+?)\s+Matrícula", texto)
    if nome_local:
#        print(nome_local.group(1)) #teste para saber se peguei o nome
        nome = nome_local.group(1)
        return nome
    else:
        print("Documento Invalido")
        return None

def ler_matricula():
    matricula_local = re.search(r"\bMatrícula:\s*(\d+)?", texto)
    if matricula_local:
#        print(matricula_local.group(1)) # teste para saber se peguei a matricula
        matricula = int(matricula_local.group(1))
        semestre = float(matricula)
        primeiro_semestre = f"{semestre:.1f}"
        return matricula
    else:
        print("Documento Invalido")
        return None

matricula = ler_matricula()
nome = ler_nome()
ira = ler_ira()
if matricula is not None:
            semestre = float(matricula)
            semestre = semestre/10000000 # Aqui eu consigo saber o primeiro semestre do aluno
            semestre = f"{semestre:.1f}"
            print(nome)
            print(matricula)
            print(semestre)
            print(ira)
