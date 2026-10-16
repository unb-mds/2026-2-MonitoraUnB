from leiturapdf import (
        arquivo_pdf,
        ler_status,
        ler_matricula,
        ler_nome,
        ler_ira,
        texto
        )

from leitura_creditos import (
        buscar_mencao,
        ler_tabela
        )

from calcular_coeficiente import calcular_coeficiente


def main():
    nome = ler_nome(texto)
    matricula = ler_matricula(texto)
    ira = ler_ira(texto)
    status = ler_status(texto)

#    print(nome)
#    print(matricula)
#    print(ira)
#    print(status)

    tabela = ler_tabela(arquivo_pdf)

    codigo = input(
            "Digite o codigo da disciplina: ")
            


    try:
        resultado = buscar_mencao(tabela, codigo)

        coeficiente = calcular_coeficiente(
            ira,
            resultado["coef_mencao"]
            )


#        print(resultado["disciplina"])
#        print(resultado["codigo"])
#        print(resultado["mencao"])
#        print(resultado["coef_mencao"])
#        print(resultado["creditos"])
#        print(resultado["periodo"])
#        print(resultado["situacao"])        tudo aqui foi teste para saber se estava funcionando
#        print(coeficiente)

    except ValueError as erro:
        print("DEU ERRO")

if __name__ == "__main__":
    main()
