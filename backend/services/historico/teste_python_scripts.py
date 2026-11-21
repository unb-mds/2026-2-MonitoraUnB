from leiturapdf import processar_historico
from leitura_creditos import (
    ler_tabela,
    buscar_mencao,
)
from calcular_coeficiente import (
    calcular_coeficiente,
)

arquivo = "/home/aquila/Downloads/historico_242023980.pdf"

# 1. Dados do estudante
aluno = processar_historico(arquivo)

print("\n=== DADOS DO ESTUDANTE ===")
print(aluno)

# 2. Leitura das disciplinas
tabela = ler_tabela(arquivo)

print(f"\nDisciplinas identificadas: {len(tabela)}")

# 3. Solicitar código manualmente
codigo = input("\nDigite o código da disciplina: ").strip().upper()

# 4. Buscar a menção
resultado = buscar_mencao(tabela, codigo)

maior_mencao = resultado["maior_mencao"]
mais_recente = resultado["mais_recente"]

print("\n=== RESULTADO DA DISCIPLINA ===")
print(f"Disciplina: {maior_mencao['disciplina']}")
print(f"Código: {maior_mencao['codigo']}")
print(f"Maior menção: {maior_mencao['mencao']}")
print(f"Período da maior menção: {maior_mencao['periodo']}")
print(f"Última aprovação: {mais_recente['periodo']}")

# 5. Calcular coeficiente
coeficiente = calcular_coeficiente(
    aluno["ira"],
    maior_mencao["coef_mencao"],
)

print("\n=== COEFICIENTE FINAL ===")
print(f"Coeficiente: {coeficiente}")
