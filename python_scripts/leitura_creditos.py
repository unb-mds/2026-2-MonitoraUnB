import re

def puxar_tabela(texto):
    #
    #
    #
    ocorrencias = list(re.finditer(r"\b24\b", texto))
    primeira_linha = re.findall(r"(\S)\s+(.+?)\s+([\d,]+)\s+(\S+)", texto)
    
    return primeira_linha
