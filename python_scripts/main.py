from leiturapdf import texto
from leitura_creditos import puxar_tabela
from leitura_creditos import mencao
from leitura_creditos import coef_mencao
from leitura_creditos import transform_mencao
from leitura_creditos import gerar_txt
from leiturapdf import arquivo_pdf

#puxar_tabela(texto)
tabela = gerar_txt(arquivo_pdf)

buscar_mencao(tabela, FGA0071, MS)




