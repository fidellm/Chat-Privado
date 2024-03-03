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
    
#    nuevo_texto = nuevo_texto[::-1]
    return nuevo_texto

def desencriptar(texto: str):
    nuevo_texto = """"""
    
    for ch in texto:
        ch = ord(ch)
        
        if ch % 2 == 0:
            ch = ch - 2
        
        ch = ch - 1
        
        nuevo_texto = nuevo_texto + chr(ch)
    
#    nuevo_texto = nuevo_texto[::-1]
    return nuevo_texto

def desencriptar_array(array: list):
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
        a = desencriptar_array(a)
        
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
    primera_conexion varchar(60),
    ultima_conexion varchar(60)
)

""")

ejecutar_comando(database, """

CREATE TABLE IF NOT EXISTS amigos (
    amigo1 varchar(30),
    amigo2 varchar(30),
    
    fecha_amistad varchar(60),
    aceptado boolean
)

""")

class Gestionar_usuarios():
    def __init__(self, database: str = "DATABASE") -> None:
        self.database = database
    
    def agregar_usuario(self, nombre:str, clave:str, primera_conexion: str= '', ultima_conexion:str= ''):
        
        nombre = encriptar(nombre)
        clave = encriptar(clave)
        primera_conexion = encriptar(primera_conexion)
        ultima_conexion = encriptar(ultima_conexion)
        
        
        if not self.existe_el_usuario(nombre= desencriptar(nombre)):
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
            ult_conexion = encriptar(lista_usuario[4])
        else:
            ult_conexion = encriptar(ult_conexion)
        
        ejecutar_comando(self.database, f"""
                UPDATE usuarios 
                SET nombre = '{nombre}',
                    clave = '{clave}',
                    ultima_conexion = '{ult_conexion}'
                WHERE rowid = {id};
                """)
        
        
    def eliminar_usuario(self, id: int):
        ejecutar_comando(self.database, f"""DELETE FROM usuarios WHERE rowid = {id}""")
        
    def eliminar_usuario_por_nombre(self, nombre: str):
        nombre = encriptar(nombre)
        ejecutar_comando(self.database, f"""DELETE FROM usuarios WHERE nombre = {nombre}""")
    
    def pedir_usuario(self, nombre: str):
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, * FROM usuarios WHERE nombre = '{encriptar(nombre)}' """)
        
        try:
            data = cursor.fetchall()[0]
        except IndexError:
            return []
        
        conexion.commit()
        
        return desencriptar_array(data)
    
    def pedir_usuario_por_id(self, id: int):
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, * FROM usuarios WHERE rowid = '{id}' """)
        
        try:
            data = cursor.fetchall()[0]
        except IndexError:
            return []
        
        conexion.commit()
        
        return desencriptar_array(data)
    
    def actualizar_ultima_conexion(self, nombre: str, ultima_conexion: str):
        lista_usuario = self.pedir_usuario(nombre)
        
        rowid = lista_usuario[0]
        
        nombre = encriptar(nombre)
        
        clave = encriptar(lista_usuario[2])
        
        primera_conexion = encriptar(lista_usuario[3])
        
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
        
        try:
            data = cursor.fetchall()
        except IndexError:
            return []
        
        conexion.commit()
        
        return desencriptar_varios_arrays(data)
    
    def listar_nombres(self):
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute("""SELECT nombre FROM usuarios""")
        
        try:
            lista = []
            data = cursor.fetchall()
            for i in data:
                lista.append(i[0])
        except IndexError:
            return []
        
        conexion.commit()
        
        return desencriptar_array(lista)
    
    def pedir_clave_por_nombre(self, nombre: str):
        conexion = sqlite3.connect(self.database)
        
        cursor = conexion.cursor()
        cursor.execute(f"""SELECT clave FROM usuarios WHERE nombre = '{encriptar(nombre)}' """)
        
        data = cursor.fetchall()[0][0]
        
        conexion.commit()
        
        return desencriptar(data)
    
    def listar_id_nombre_clave(self):
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute("""SELECT rowid, nombre, clave FROM usuarios""")
        
        try:
            data = cursor.fetchall()
        except IndexError:
            return []
        
        conexion.commit()
        
        return desencriptar_varios_arrays(data)
    
    def listar_id_nombre_clave_por_id(self, id: int):
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, nombre, clave FROM usuarios WHERE rowid = {id}""")
        
        data = cursor.fetchall()[0]
        
        conexion.commit()
        
        return desencriptar_array(data)
    
    def listar_id_nombre_primera_ultima_conexion(self):
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute("""SELECT rowid, nombre, primera_conexion, ultima_conexion FROM usuarios""")
        
        data = cursor.fetchall()
        
        conexion.commit()
        
        return desencriptar_varios_arrays(data)
    
    def obtener_id_por_nombre(self, nombre: str):
        nombre = encriptar(nombre)

        try:
            conexion = sqlite3.connect(self.database)

            cursor = conexion.cursor()
            cursor.execute(f"""SELECT rowid FROM usuarios WHERE nombre = '{nombre}'""")
            
            data = cursor.fetchall()[0][0]
            
            conexion.commit()
            
            return data
        except:
            return None
    
    def existe_el_usuario(self, nombre: str):
        #print(self.listar_nombres())
        try:
            for i in self.listar_nombres():
                if i.lower() == nombre.lower():
                    return True
        except IndexError:
            pass

        return False
    
    def es_el_usuario(self, nombre: str, clave: str):
        if self.existe_el_usuario(nombre):
            return self.pedir_clave_por_nombre(nombre) == clave
        
        return False

class Gestionar_Amigos():
    def __init__(self, database: str = "DATABASE") -> None:
        self.database = database
    
    
    def mandar_solicitud_de_amistad(self, amigo1: str, amigo2: str):

        amigo1 = encriptar(amigo1)
        amigo2 = encriptar(amigo2)

        ejecutar_comando(self.database, f"""
                         INSERT INTO amigos (amigo1, amigo2, fecha_amistad, aceptado) VALUES (
                            '{amigo1}', '{amigo2}', '', {False}
                         )
                         """)
    
    def eliminar_solicitud_o_amistad(self, amigo1: str, amigo2: str):
        amigo1 = encriptar(amigo1)
        amigo2 = encriptar(amigo2)
        
        
        ejecutar_comando(self.database, f"""DELETE FROM amigos WHERE amigo1 = '{amigo1}' AND amigo2 = '{amigo2}' """)
        ejecutar_comando(self.database, f"""DELETE FROM amigos WHERE amigo2 = '{amigo1}' AND amigo1 = '{amigo2}' """)
    
    def aceptar_solicitud(self, amigo1: str, amigo2: str, fecha_amistad: str):
        amigo1 = encriptar(amigo1)
        amigo2 = encriptar(amigo2)
        fecha_amistad = encriptar(fecha_amistad)
    
        
        ejecutar_comando(self.database, f"""UPDATE amigos 
                         SET aceptado = {True}, fecha_amistad = '{fecha_amistad}' WHERE amigo1 = '{amigo1}' AND amigo2 = '{amigo2}' """)
        
    def listar_solicitudes(self):
        
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, * FROM amigos WHERE aceptado = {False}""")
        
        try:
            data = cursor.fetchall()
        except IndexError:
            return []
        
        conexion.commit()
        
        return desencriptar_varios_arrays(data)
        
    def listar_amistades(self):
        
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, * FROM amigos WHERE aceptado = {True}""")
        
        try:
            data = cursor.fetchall()
        except IndexError:
            return []
        
        conexion.commit()
        
        return desencriptar_varios_arrays(data)
        
print(Gestionar_usuarios().listar_id_nombre_clave())

#Gestionar_Amigos().mandar_solicitud_de_amistad('Fidel', 'Nacho')

#Gestionar_Amigos().aceptar_solicitud('Fidel', 'Nacho', 'ayer xdd')
#print(Gestionar_Amigos().listar_amistades())



#print(encriptar(Gestionar_usuarios().pedir_clave_por_nombre('Fidelito')))

