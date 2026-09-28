import re
from pypdf import PdfReader
from leiturapdf import texto

SITUACOES = {
    "APR": "Aprovado",
    "REP": "Reprovado por média",
    "REPF": "Reprovado por falta",
    "REPMF": "Reprovado por média e falta",
    "MATR": "Matriculado (em andamento)",
    "TRANC": "Trancado",
    "CANC": "Cancelado",
    "DISP": "Dispensado",
    "CUMP": "Cumpriu por aproveitamento", 
}

def puxar_tabela(texto):
    #Extrai as linhas de disciplinas do historico SIGAA em modo layout

    inicio = re.compile(
            r"^\s*(?P<periodo>\d{4}[./]\d+)\s+"
            r"(?:[*e&#@§%]\s*)?"
            r"(?P<codigo>[A-Z]+\d+|\d{4,}|ENADE)\s+"
            r"(?P<resto>.*)$"
            )
    colunas = re.compile(
            r"(?P<disciplina>.+?)\s+"
            r"(?P<ch>\d+)\s+\S+\s+(?:\d+(?:[.,]\d+)?|-+)\s+"
            r"(?P<mencao>[A-Z]+|\d+(?:[.,]\d+)?|-+)\s+(?P<sigla>[A-Z]+)"
            )
    disciplinas = []
    pendente = None
    for linha in texto.splitlines():
        if re.match(r"^\s*\d{4}[./]\d+/b", linha):
            if pendente is not None:
                raise ValueError(
                    f"Não foi possível interpretar {pendente['codigo']} "
                    f"no período {pendente['periodo']}. Confira o layout do PDF."
                )
            registro = inicio.fullmatch(linha)
            if registro is None:
                raise ValueError(f"Linha de disciplina não reconhecida: {linha.strip()}")
            if registro["codigo"] == "ENADE":
                continue
            pendente = registro.groupdict()
        elif pendente is not None:
            pendente["resto"] += " " + linha.strip()
        else:
            continue
    
        resultado = colunas.fullmatch(pendente["resto"].strip())
        if resultado is None:
            continue
        dados = resultado.groupdict()
        dados["periodo"] = pendente["periodo"].replace("/", ".")
        dados["codigo"] = pendente["codigo"]
        dados["disciplina"] = " ".join(dados["disciplina"].split())
        dados["ch"] = int(dados["ch"])
        #precisamos dividir as horas em creditos, que no caso seriam dividir as horas por 15




    ocorrencias = list(re.finditer(r"\b24\b", texto))
    primeira_linha = re.findall(r"(\S)\s+(.+?)\s+([\d,]+)\s+(\S+)", texto)
    print(primeira_linha)

puxar_tabela(texto)
