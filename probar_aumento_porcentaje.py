

def calcular_aumento(valor_inicial: float, valor_final: float):    
    diferencia = valor_final - valor_inicial

    aumento = (diferencia / abs(primer_mes))
    return aumento


primer_mes = 11258.06
segundo_mes = 56322.5

print(calcular_aumento(primer_mes, segundo_mes))

