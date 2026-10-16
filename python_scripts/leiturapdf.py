import re
from pypdf import PdfReader
from pathlib import Path

caminho_pdf = Path("~/Projetos/historico26.2.pdf").expanduser()

arquivo_pdf = PdfReader(caminho_pdf)

texto = arquivo_pdf.pages[0].extract_text(extraction_mode="layout")

def ler_status(texto):           # o aluno precisa obrigatoriamente estar com o status como ativo para poder se matricular
    status_local = re.search(
            r"\b(ATIVO|FORMANDO|TRANCADO|CADASTRADO|CANCELADO|DESLIGADO)\b",
            texto,
            re.IGNORECASE
            )

    if status_local:
        status = status_local.group(1).strip().upper()
        return status

    return None

#quero vir aqui deixar a minha indignacao sobre essa leitura de pdf que PELO AMOR DE DEUS QUE COISA DIFICIL EU DEMOREI DOIS DIAS PARA PEGAR NOME IRA E MATRICULA

def ler_ira(texto):
    ira_local = re.search(r"\bIRA:\s*(\d+(?:[.,]\d+)?)", texto)
    if ira_local:
#        print(ira_local.group(1)) # teste para saber se peguei o ira
        ira = float(ira_local.group(1).replace(",", "."))
        return ira
    else:
        print("Documento Invalido") #colocar acentos #ainda nao coloquei acentos, estou com preguica do teclado us
        return None

def ler_nome(texto):
    nome_local = re.search(r"\bNome:\s*(.+?)\s+Matrícula", texto)
    if nome_local:
#        print(nome_local.group(1)) #teste para saber se peguei o nome
        nome = nome_local.group(1)
        return nome
    else:
        print("Documento Invalido")
        return None

def ler_matricula(texto):
    matricula_local = re.search(r"\bMatrícula:\s*(\d+)", texto)
    if matricula_local:
#        print(matricula_local.group(1)) # teste para saber se peguei a matricula
        matricula = int(matricula_local.group(1))
#        semestre = float(matricula)
#        primeiro_semestre = f"{semestre:.1f}"
        return matricula
    else:
        print("Documento Invalido")
        return None

matricula = ler_matricula(texto)
nome = ler_nome(texto)
ira = ler_ira(texto)

# TESTE DE MATRICULA, IRA E NOME
#
#if matricula is not None:
#            semestre = float(matricula)
#            semestre = semestre/10000000 # Aqui eu consigo saber o primeiro semestre do aluno
#            semestre = f"{semestre:.1f}"
#            print(nome)
#            print(matricula)
#            print(semestre)
#            print(ira)
