
def calcular_numero_mayor(arreglo: list):
    print(arreglo)
    
    while len(arreglo) > 1:
        num1 = arreglo[0]
        num2 = arreglo[1]
        
        if num1 > num2:
            arreglo.pop(-1)
        elif num2 > num1:
            arreglo.pop(0)
        else:
            arreglo.pop(0)
    
    return arreglo[0]


arreglo_probar = [12, 14, 40, 3, 2, 5, 9, 29, 4, 5, 4, 4, 4, 60, 10, -12, -80, 4, 20, 1, 3, 4, 20, 6, 20]
numero_mayor = calcular_numero_mayor(arreglo_probar)

print(numero_mayor)

