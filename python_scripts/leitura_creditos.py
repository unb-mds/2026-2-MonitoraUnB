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
        dados["creditos"] = dados["ch"] / 15
        dados["situacao"] = SITUACOES.get(dados["sigla"],  "Situação desconhecida")
        disciplinas.append(dados)
        pendente = None
    if pendente is not None:
        raise ValueError(
            f"Não foi possível interpretar {pendente['codigo']} "
            f"no período {pendente['periodo']}. Confira o layout do PDF."
                )
    return disciplinas

def gerar_txt(arquivo_pdf, arquivo_txt=None):
    arquivo_pdf = Path(arquivo_pdf)
    if arquivo_txt is None:
        arquivo_txt = arquivo_pdf.with_name(f"{arquivo_pdf.stem}_disciplinas.txt")
    arquivo_txt = Path(arquivo_txt)
    if arquivo_pdf.resolve() == arquivo_txt.resolve()
        raise ValueError("O arquivo de saída não pode ser o próprio PDF.")
    if arquivo_txt.suffix.lower() != ".txt":
        raise ValueError("O arquivo de saída deve ter a extensão .txt.")

    historico = PdfReader(arquivo_pdf)
    disciplinas = []
    for numero, pagina in enumerate(historico.pages, start=1):
        texto = pagina.extract_text(extraction_mode="layout") or ""
        if not texto.strip():
            raise ValueError(
                f"A página {numero} não contém texto extraível. "
                "Para evitar uma tabela incompleta, a extração foi interrompida. "
                "Se a página for digitalizada, será necessário OCR."
            )
        try:
            disciplinas.extend(puxar_tabela(texto))
        except ValueError as erro:
            raise ValueError(f"Página {numero}: {erro}") from erro

    if not disciplinas:
        raise ValueError(
            "Nenhuma disciplina encontrada. Verifique se o PDF é um histórico "
            "SIGAA com texto selecionável; PDFs digitalizados precisam de OCR."
        )

    linhas = [["Período", "Código", "Disciplina", "CH (h)", "Créditos", "Menção", "Situação"]]
    for disciplina in disciplinas:
        linhas.append([
            disciplina["periodo"],
            disciplina["codigo"],
            disciplina["disciplina"],
            str(disciplina["ch"]),
            f'{disciplina["creditos"]:g}',
            disciplina["mencao"],
            f'{disciplina["sigla"]} - {disciplina["situacao"]}',
        ])

    larguras = [max(len(valor) for valor in coluna) for coluna in zip(*linhas)]
    tabela = [
            " | ".join(valor.ljust(largura) for valor, largura in zip(linha, larguras))
            for linha in linhas
    ]
    tabela.insert(1, "-+-".join("-" * largura for largura in larguras))
    cabecalho = (
        "DISCIPLINAS DO HISTÓRICO ESCOLAR\n"
        "Créditos calculados: carga horária / 15 (1 crédito = 15 horas).\n"
        "Cada linha representa uma tentativa no período indicado.\n"
        "MATR e TRANC não significam reprovação; '-' indica menção não informada.\n\n"
        )
    arquivo_txt.write_text(cabecalho + "\n".join(tabela) + "\n", enconding = "utf-8")
    return disciplinas

#MUDAR O CODIGO PARA IMEDIATAMENTE APAGAR O TXT PARA NAO COMPROMETER AS INFORMCACOES DO ESTUDANTE 
