
def calcular_precio(costo: float, margen: float):
    return costo / (1 - (margen / 100) )


precio_sin_impuestos = calcular_precio(47, 30)

impuesto = 20 / 100
precio_con_impuestos = precio_sin_impuestos + ( precio_sin_impuestos * impuesto)

print(precio_sin_impuestos)
print(precio_con_impuestos)

