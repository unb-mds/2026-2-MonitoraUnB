def calcular_coeficiente(ira, coef_mencao):
    if ira is None:
        raise ValueError("IRA nao encontrado.")

    if coef_mencao is None:
        raise ValueError("Mencao nao encontrada")

    coeficiente = (ira * 0.6) + (coef_mencao * 0.4)

    return round(coeficiente, 4)
