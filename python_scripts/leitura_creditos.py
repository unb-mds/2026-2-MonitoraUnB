import re
from pypdf import PdfReader
from leiturapdf import texto

def puxar_tabela(texto):
    #
    #
    #
    ocorrencias = list(re.finditer(r"\b24\b", texto))
    primeira_linha = re.findall(r"(\S)\s+(.+?)\s+([\d,]+)\s+(\S+)", texto)
    print(primeira_linha)

puxar_tabela(texto)
