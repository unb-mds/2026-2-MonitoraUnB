from backend.services.historico.leitura_creditos import ler_tabela
from pypdf import PdfReader

historico = PdfReader(
    "C:\curso ALURA\MDS\historico_251022427.pdf"
)

tabela = ler_tabela(historico)

print(tabela)