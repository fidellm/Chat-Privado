import sqlite3

database = "DATABASE"

def encriptar(texto: str):
    nuevo_texto = """"""
    
    for ch in texto:
        ch = ord(ch)
        
        ch = ch + 1
        
        if ch % 2 == 0:
            ch = ch + 2
        
        nuevo_texto = nuevo_texto + chr(ch)
    
    return nuevo_texto

def desencriptar(texto: str):
    nuevo_texto = """"""
    
    for ch in texto:
        ch = ord(ch)
        
        if ch % 2 == 0:
            ch = ch - 2
        
        ch = ch - 1
        
        nuevo_texto = nuevo_texto + chr(ch)
    
    return nuevo_texto

def desecriptar_array(array):
    nuevo_array = []
    
    for a in array:
        try:
            a = desencriptar(a)
        except:
            pass
        nuevo_array.append(a)
        
    return nuevo_array

def desencriptar_varios_arrays(array):
    nuevo_array = []
    
    for a in array:
        a = desecriptar_array(a)
        
        nuevo_array.append(a)
    
    return nuevo_array




def ejecutar_comando(db, comando):
    conexion = sqlite3.connect(db)

    cursor = conexion.cursor()
    cursor.execute(comando)
    
    conexion.commit()
    
ejecutar_comando(database, """

CREATE TABLE IF NOT EXISTS usuarios (
    nombre varchar(30),
    clave varchar(50),
    primera_conexion varchar(40),
    ultima_conexion varchar(40)
)

""")

ejecutar_comando(database, """

CREATE TABLE IF NOT EXISTS amigos (
    string_amigos varchar(31),
    
    fecha_amistad varchar(40),
    pendiente boolean
)

""")

class Gestionar_usuarios():
    def __init__(self, database: str = "DATABASE") -> None:
        self.database = database
    
    def agregar_usuario(self, nombre:str, clave:str, primera_conexion: str, ultima_conexion:str):
        nombre = encriptar(nombre)
        clave = encriptar(clave)
        primera_conexion = encriptar(primera_conexion)
        ultima_conexion = encriptar(ultima_conexion)
        
        ejecutar_comando(self.database, f"""
                         INSERT INTO usuarios (nombre, clave, primera_conexion, ultima_conexion) VALUES (
                             '{nombre}', '{clave}', '{primera_conexion}', '{ultima_conexion}'
                         );
                         """)
    
    def actualizar_usuario(self, id: int, nombre, clave, ult_conexion=None):
        lista_usuario = self.pedir_usuario(nombre)
        
        nombre = encriptar(nombre)
        clave = encriptar(clave)
            
        if ult_conexion == None:
            ult_conexion = lista_usuario[4]
        else:
            ult_conexion = encriptar(ult_conexion)
        
        ejecutar_comando(self.database, f"""
                UPDATE usuarios 
                SET nombre = '{nombre}',
                    clave = '{clave}',
                    ultima_conexion = '{ult_conexion}'
                WHERE rowid = {id};
                """)
        
        
    def eliminar_usuario(self, id):
        ejecutar_comando(self.database, f"""DELETE FROM usuarios WHERE rowid = {id}""")
    
    def pedir_usuario(self, nombre):
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, * FROM usuarios WHERE nombre = '{encriptar(nombre)}' """)
        
        data = cursor.fetchall()[0]
        
        conexion.commit()
        
        return data
    
    def actualizar_ultima_conexion(self, nombre: str, ultima_conexion: str):
        lista_usuario = self.pedir_usuario(nombre)
        
        rowid = lista_usuario[0]
        
        nombre = encriptar(nombre)
        
        clave = lista_usuario[2]
        
        primera_conexion = lista_usuario[3]
        
        ultima_conexion = encriptar(ultima_conexion)
        
        
        ejecutar_comando(self.database, f"""
                UPDATE usuarios 
                SET nombre = '{nombre}',
                    clave = '{clave}',
                    primera_conexion = '{primera_conexion}',
                    ultima_conexion = '{ultima_conexion}'
                WHERE rowid = {rowid};
                """)
    
    def listar_usuarios(self):
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute("""SELECT rowid, * FROM usuarios""")
        
        data = cursor.fetchall()
        
        conexion.commit()
        
        return data
    
    def listar_nombres(self):
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute("""SELECT nombre FROM usuarios""")
        
        data = cursor.fetchall()[0]
        
        conexion.commit()
        
        return data
    
    def pedir_clave_por_nombre(self, nombre: str):
        conexion = sqlite3.connect(self.database)
        
        cursor = conexion.cursor()
        cursor.execute(f"""SELECT clave FROM usuarios WHERE nombre = '{encriptar(nombre)}' """)
        
        data = cursor.fetchall()[0][0]
        
        conexion.commit()
        
        return data
    
    def listar_id_nombre_clave(self):
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute("""SELECT rowid, nombre, clave FROM usuarios""")
        
        data = cursor.fetchall()
        
        conexion.commit()
        
        return data
    
    def listar_id_nombre_clave_por_id(self, id: int):
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, nombre, clave FROM usuarios WHERE rowid = {id}""")
        
        data = cursor.fetchall()[0]
        
        conexion.commit()
        
        return data
    
    def listar_id_nombre_primera_ultima_conexion(self):
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute("""SELECT rowid, nombre, primera_conexion, ultima_conexion FROM usuarios""")
        
        data = cursor.fetchall()
        
        conexion.commit()
        
        return data
    
    def existe_el_usuario(self, nombre: str):
        for i in self.listar_nombres():
            if desencriptar(i).lower() == nombre.lower():
                return True

        return False
    
    def es_el_usuario(self, nombre: str, clave: str):
        if self.existe_el_usuario(nombre):
            return self.pedir_clave_por_nombre(nombre) == encriptar(clave)
        
        return False

class Gestionar_Amigos():
    def __init__(self, database: str = "DATABASE") -> None:
        self.database = database
    
    
    def mandar_solicitud_de_amistad(self, amigo1: str, amigo2: str):
        #string_amigos en un ejemplo sería "roberto carlos" pero los nombres encriptados.
        #en los nombres es imposible que siendo encriptados tengan espacios porque el
        # espacio es el primer caracter ascii y
        # al ecriptarse se suman los caracteres


        string_amigos = encriptar(amigo1 + " " + amigo2)

        ejecutar_comando(self.database, f"""
                         INSERT INTO amigos (string_amigos, fecha_amistad, pendiente) VALUES (
                             '{string_amigos}', '', {False}
                         )
                         """)
    
    def eliminar_solicitud_o_amistad(self, amigo1: str, amigo2: str):
        amigo1 = encriptar(amigo1)
        amigo2 = encriptar(amigo2)
        
        string_amigos = amigo1 + " " + amigo2
        
        ejecutar_comando(self.database, f"""DELETE FROM amigos WHERE string_amigos = '{string_amigos}'""")
    
    def aceptar_solicitud(self, amigo1: str, amigo2: str, fecha_amistad: str):
        amigo1 = encriptar(amigo1)
        amigo2 = encriptar(amigo2)
        fecha_amistad = encriptar(fecha_amistad)
        
        string_amigos = amigo1 + " " + amigo2
        
        ejecutar_comando(self.database, f"""UPDATE amigos 
                         SET pendiente = {True}, fecha_amistad = '{fecha_amistad}' WHERE string_amigos = '{string_amigos}'""")
        
    def listar_solicitudes(self):
        
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, * FROM amigos WHERE pendiente = {False}""")
        
        data = cursor.fetchall()
        
        conexion.commit()
        
        return data
        
    def listar_amistades(self):
        
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, * FROM amigos WHERE pendiente = {True}""")
        
        data = cursor.fetchall()
        
        conexion.commit()
        
        return data
        

#gestionar = Gestionar_Amigos()

#variable = gestionar.mandar_solicitud_amigo("Filo", "Bravo")

#variable = gestionar.listar_solicitudes()
#print(desencriptar_varios_arrays(variable))

print(desecriptar_array(Gestionar_usuarios().listar_nombres()))