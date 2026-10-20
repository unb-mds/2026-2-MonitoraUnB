import re
from pypdf import PdfReader 

'''Dicionário de Siglas'''

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

#
# o que precisamos colocar, precisamos colocar os erros, caso um aluno coloque uma materia que ele esta cursando, foi reprovado ou foi trancado
#

MENCOES = {
    "SS": 5,
    "MS": 4,
    "MM": 3,
    "MI": 2,
    "II": 1,
    "SR": 0,
        }


def buscar_aprovacao(tabela, codigo):
    codigo = codigo.strip().upper()
    global mencao
    global coef_mencao
    mencao = None
    coef_mencao = None

    for disciplina in tabela:
        if disciplina["codigo"] == codigo:

            situacao = disciplina["situacao"].strip().upper()

            if situacao != "APROVADO":
            #qualquer coisa diferente de aprovado ele vai negar a possibilidade de matricula naquela materia
            #obs para o aquila do futuro ou qualquer um que vai usar o codigo, adicionar cumpriu por aproveitamento, mas isso vai estar encaixado no quesito de equivalentes
                return None

            mencao = disciplina["mencao"].strip().upper()
            coef_mencao = MENCOES.get(mencao)

            return {
                    "codigo": disciplina["codigo"],
                    "disciplina": disciplina["disciplina"],
                    "mencao": disciplina["mencao"],
                    "creditos": disciplina["creditos"]
                    }



    return None

def puxar_tabela(texto): 
    padrao_inicio = re.compile(
        r"^\s*(?P<periodo>\d{4}[./]\d+)\s+"
        r"(?:[*e&#@§%]\s*)?"
        r"(?P<codigo>[A-Z]+\d+|\d{4,}|ENADE)\s+"
        r"(?P<resto>.*)$"
    )

    padrao_colunas = re.compile(
        r"(?P<disciplina>.+?)\s+"
        r"(?P<ch>\d+)\s+\S+\s+"
        r"(?:\d+(?:[.,]\d+)?|-+)\s+"
        r"(?P<mencao>[A-Z]+|\d+(?:[.,]\d+)?|-+)\s+"
        r"(?P<sigla>[A-Z]+)"
    )

    disciplinas = {}
    pendente = None

    for linha in texto.splitlines():
        inicio = padrao_inicio.fullmatch(linha)

        if inicio is not None:

            if pendente is not None:
                raise ValueError(
                        f"Não foi possível interpretar"
                        f"{pendente['codigo']}."
                        )
            if inicio['codigo'] == "ENADE":
                continue

            pendente = inicio.groupdict()

        elif pendente is not None:
            pendente["resto"] += " " + linha.strip()

        else: continue

        resultado = padrao_colunas.fullmatch(
                pendente["resto"].strip()
                )

        if resultado is None:
            continue


        dados = resultado.groupdict()
        dados["periodo"] = pendente["periodo"].replace("/", ".")
        dados["codigo"] = pendente["codigo"]
        dados["disciplina"] = " ".join(dados["disciplina"].split())
        dados["ch"] = int(dados["ch"])
        '''Divide-se as horas por 15 para obter os créditos'''
        dados["creditos"] = dados["ch"] / 15

        dados["situacao"] = SITUACOES.get(dados["sigla"],  "Situação desconhecida")
        mencao = dados["mencao"].strip().upper()
        dados["coef_mencao"] = MENCOES.get(mencao)

        codigo = dados["codigo"]

        if codigo not in disciplinas:
            disciplinas[codigo] = []

        disciplinas[codigo].append(dados)

        pendente = None

    if pendente is not None:
        raise ValueError(
            f"Não foi possível interpretar {pendente['codigo']} "
            f"no período {pendente['periodo']}. Confira o layout do PDF."
                )
    return disciplinas

def ler_tabela(arquivo_pdf):
    historico = PdfReader(arquivo_pdf)

    disciplinas = {}

    for numero, pagina in enumerate(
            historico.pages, start = 1
            ):

        texto = pagina.extract_text(
                extraction_mode="layout"
                ) or ""

        if not texto.strip():
            raise ValueError(
                    f"Página {numero} sem texto extraível"
                    )

        try:
            dados_pagina = puxar_tabela(texto)

        except ValueError as erro:
            raise ValueError(
                    f"Erro na página {numero}: {erro}"
                    ) from erro

        for codigo, tentativas in dados_pagina.items():
            if codigo not in disciplinas:
                disciplinas[codigo] = []


            disciplinas[codigo].extend(tentativas)

        if not disciplinas:
            raise ValueError(
                    "Nenhuma disciplina encontrada no histórico."
                    )
    return disciplinas


def buscar_disciplinas(tabela, codigo):
    codigo = codigo.strip().upper()

    return tabela.get(codigo, [])

def buscar_mencao(tabela, codigo):
    tentativas = buscar_disciplinas(tabela, codigo)

    if not tentativas:
        raise ValueError(
                f"Disciplina {codigo} não encontrada"
                )

    aprovadas = [
            tentativa
            for tentativa in tentativas
            if tentativa["sigla"] == "APR"
            and tentativa["coef_mencao"] is not None
            ]

    def obter_periodo(disciplina):
        ano, semestre = disciplina["periodo"].split(".")
        return (int(ano), int(semestre))

    def obter_coeficiente(disciplina):
        return disciplina["coef_mencao"]

    if not aprovadas:
        ultima = max(tentativas, key=obter_periodo)

        raise ValueError(
                f"Disciplina {codigo} sem aprovação."
                f"Última situação: {ultima['situacao']}."
                )

    mais_recente = max (
            aprovadas,
            key=obter_periodo
            )

    maior_mencao = max(
            aprovadas,
            key=obter_coeficiente
            )

    return {
            "mais_recente": mais_recente,
            "maior_mencao": maior_mencao
            }
