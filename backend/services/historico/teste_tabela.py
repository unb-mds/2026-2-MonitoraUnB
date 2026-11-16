from backend.services.historico.leitura_creditos import ler_tabela
from pypdf import PdfReader
from calcular_coeficiente import calcular_coeficiente


historico = PdfReader(
#"C:\curso ALURA\MDS\historico_251022427.pdf"
    "~/Downloads/historico_242023980.pdf"
)

tabela = ler_tabela(historico)

print(tabela)
