
def encriptar_caracter(ch: str):
    num_ascii = ord(ch)
    
    num_ascii += 1
    
    return ascii(num_ascii)
    
def desencriptar_caracter(ch: str):
    num_ascii = ord(ch)
    
    num_ascii -= 1
    
    return ascii(num_ascii)
    

def encriptar_texto(texto: str):
    retornar = ''
    
    for ch in texto:
        retornar += encriptar_caracter(ch)
        
    return retornar

def desencriptar_texto(texto: str):
    retornar = ''
    
    for ch in texto:
        retornar += desencriptar_caracter(ch)
        
    return retornar

text = 'Holaa a todosss :), xdd, arroz papa huevo'

text = encriptar_texto(text)
print(text)

print('')

print(desencriptar_texto(text))