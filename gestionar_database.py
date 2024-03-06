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
    
    fecha_amistad varchar(100),
    aceptado boolean
)

""")

ejecutar_comando(database, """

CREATE TABLE IF NOT EXISTS chats_privados (
    amigo1 varchar(30),
    amigo2 varchar(30),
    chat_visible boolean,
    quiere_ocultar_chat boolean
)

""")

ejecutar_comando(database, """

CREATE TABLE IF NOT EXISTS mensajes_chats_privados (
    emisor varchar(30),
    fecha varchar(100),
    
    mensaje Text(300),
    es_visible boolean,
    
    chat_privado_id int
    
)

""")

class Gestionar_usuarios():
    def __init__(self) -> None:
        self.database = "DATABASE"
    
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
    def __init__(self) -> None:
        self.database = "DATABASE"
    
    
    def mandar_solicitud_de_amistad(self, amigo1: str, amigo2: str):
        
        if not self.es_su_amigo_o_solicitud(amigo1, amigo2):
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
    
    def eliminar_solicitud_o_amistad_por_id(self, id: int):
        ejecutar_comando(self.database, f"""DELETE FROM amigos WHERE rowid = {id} """)
        
    def cancelar_solicitud_de_amistad_por_id(self, amigo1: str, id: int):
        amigo1 = encriptar(amigo1)
        
        ejecutar_comando(self.database, f"""DELETE FROM amigos WHERE rowid = {id} AND amigo1 = '{amigo1}' AND aceptado = {False}""")
    
    def aceptar_solicitud(self, amigo1: str, amigo2: str, fecha_amistad: str):
        amigo1 = encriptar(amigo1)
        amigo2 = encriptar(amigo2)
        fecha_amistad = encriptar(fecha_amistad)
    
        
        ejecutar_comando(self.database, f"""UPDATE amigos 
                         SET aceptado = {True}, fecha_amistad = '{fecha_amistad}' WHERE amigo1 = '{amigo1}' AND amigo2 = '{amigo2}' """)
        
    def obtener_solicitud_o_amistad(self, amigo1: str, amigo2: str):
        amigo1 = encriptar(amigo1)
        amigo2 = encriptar(amigo2)
        
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, * FROM amigos WHERE (amigo1 = '{amigo1}' AND amigo2 = '{amigo2}') 
                                                          OR (amigo2 = '{amigo1}' AND amigo1 = '{amigo2}') """)
        
        try:
            data = cursor.fetchall()[0]
        except IndexError:
            return []
        
        conexion.commit()
        
        return desencriptar_array(data)
        
    def obtener_solicitud_o_amistad_por_id(self, id: int):
        
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, * FROM amigos WHERE rowid = {id} """)
        
        try:
            data = cursor.fetchall()[0]
        except IndexError:
            return []
        
        conexion.commit()
        
        return desencriptar_array(data)
    
    
    def es_su_amigo_o_solicitud(self, amigo1: str, amigo2: str):
        lista_amistad = self.obtener_solicitud_o_amistad(amigo1, amigo2)
        
        return lista_amistad != []
    
    def es_su_amigo_o_solicitud_por_id(self, amigo: str, id: int):
        lista_amistad = self.obtener_solicitud_o_amistad_por_id(id)
        
        return lista_amistad[1] == amigo or lista_amistad[2] == amigo
    
    def es_su_amigo(self, amigo1: str, amigo2: str):
        
        lista_amistad = self.obtener_solicitud_o_amistad(amigo1, amigo2)
        
        return lista_amistad[4]
    
    def es_su_amigo_por_id(self, amigo: str, id: int):
        
        lista_amistad = self.obtener_solicitud_o_amistad_por_id(id)
        
        return lista_amistad[4] and (lista_amistad[1] == amigo or lista_amistad[2] == amigo)
    
    
    def es_su_solicitud_por_id(self, amigo1: str, id: int):
        lista_amistad = self.obtener_solicitud_o_amistad_por_id(id)
        print(lista_amistad)
        
        return (not lista_amistad[4]) and (lista_amistad[1] == amigo1)
    
    def es_la_solicitud_hacia_el_por_id(self, amigo2: str, id: int):
        lista_amistad = self.obtener_solicitud_o_amistad_por_id(id)
        
        return (not lista_amistad[4]) and (lista_amistad[2] == amigo2)
    
    def es_la_solicitud_hacia_el(self, amigo1: str, amigo2: str):
        lista_amistad = self.obtener_solicitud_o_amistad_por_id(id)
        
        return (not lista_amistad[4]) and (lista_amistad[1] == amigo1 and lista_amistad[2] == amigo2)
    
    
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
    
    def listar_solicitudes_hacia_un_usuario(self, nombre: str):
        nombre = encriptar(nombre)
        
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, * FROM amigos WHERE aceptado = {False} AND amigo2 = '{nombre}' """)
        
        try:
            data = cursor.fetchall()
                
            conexion.commit()
        except IndexError:
            return []
        
        
        return desencriptar_varios_arrays(data)
    
    def listar_solicitudes_de_un_usuario(self, nombre: str):
        nombre = encriptar(nombre)
        
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, * FROM amigos WHERE aceptado = {False} AND amigo1 = '{nombre}' """)
        
        try:
            data = cursor.fetchall()
                
            conexion.commit()
        except IndexError:
            return []
        
        
        return desencriptar_varios_arrays(data)
    
    def listar_amistades_de_un_usuario(self, nombre: str):
        
        nombre = encriptar(nombre)
        
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, * FROM amigos WHERE aceptado = {True} AND (amigo1 = '{nombre}' OR amigo2 = '{nombre}')""")
        
        try:
            data = cursor.fetchall()
                
            conexion.commit()
        except IndexError:
            return []
        
        
        return desencriptar_varios_arrays(data)


class Gestionar_chats_privados():
    def __init__(self) -> None:
        self.database = "DATABASE"
    
    def crear_chat_privado(self, amigo1: str, amigo2: str):
        if not self.existe_el_chat_privado(amigo1, amigo2):
            amigo1 = encriptar(amigo1)
            amigo2 = encriptar(amigo2)
            
            ejecutar_comando(self.database, f"""
                                INSERT INTO chats_privados (amigo1, amigo2) VALUES (
                                    '{amigo1}', '{amigo2}'
                                );
                                """)
            
    def eliminar_chat_privado_por_id(self, chat_id):
        ejecutar_comando(self.database, f"""DELETE FROM chats_privados WHERE rowid = {chat_id} """)
        
    
    def obtener_id_chat_privado(self, amigo1: str, amigo2: str):
        amigo1 = encriptar(amigo1)
        amigo2 = encriptar(amigo2)

        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid FROM chats_privados WHERE (amigo1 = '{amigo1}' AND amigo2 = '{amigo2}') 
                                                               OR (amigo2 = '{amigo1}' AND amigo1 = '{amigo2}')""")
        
        data = cursor.fetchall()[0][0]
            
        conexion.commit()
    
        
        return data
    
    def agregar_mensaje_chat_privado_por_id(self, emisor: str, fecha_mensaje: str, mensaje: str, chat_id: int):
        emisor = encriptar(emisor)
        fecha_mensaje = encriptar(fecha_mensaje)
        mensaje = encriptar(mensaje)
        
        ejecutar_comando(self.database, f"""
                        INSERT INTO mensajes_chats_privados (emisor, fecha, mensaje, chat_privado_id) VALUES (
                            '{emisor}', '{fecha_mensaje}', '{mensaje}', {chat_id}
                        )
                        """)
        
    def eliminar_mensaje_por_id(self, emisor: str, mensaje_id: int, chat_id: int):
        emisor = encriptar(emisor)
        
        ejecutar_comando(self.database, f"""
                        DELETE FROM mensajes_chats_privados WHERE rowid = {mensaje_id} AND chat_privado_id = {chat_id} AND emisor = '{emisor}' """)
        
    def eliminar_todos_los_mensajes_por_chat_id(self, chat_id: int):
        ejecutar_comando(self.database, f"""
                        DELETE FROM mensajes_chats_privados WHERE chat_privado_id = {chat_id}""")
    
    def eliminar_todos_los_mensajes_de_un_chat(self, amigo1: str, amigo2: str):
        amigo1 = encriptar(amigo1)
        amigo2 = encriptar(amigo2)
        
        ejecutar_comando(self.database, f"""
                        DELETE FROM mensajes_chats_privados WHERE (amigo1 = '{amigo1}' AND amigo2 = '{amigo2}')
                                                               OR (amigo2 = '{amigo1}' AND amigo1 = '{amigo2}')""")
    
    
    def obtener_mensajes_chat_privado_por_id(self, chat_id: int):
        
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, * FROM mensajes_chats_privados WHERE chat_privado_id = {chat_id}""")
        
        try:
            data = cursor.fetchall()
        
            conexion.commit()
            
            data = desencriptar_varios_arrays(data)
            
        
        except IndexError:
            return []
    
        chat_adaptado = []
        
        for message in data:
            nuevo_mensaje = {"id_message": message[0], "timestamp": message[2], "from": message[1], "message":message[3], "visible": message[4]}
            chat_adaptado.append(nuevo_mensaje)
        
        return chat_adaptado


    def obtener_datos_chat_privado_por_id(self, chat_id: int):
        
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, * FROM chats_privados WHERE rowid = {chat_id}""")
        
        try:
            data = cursor.fetchall()[0]
        
            conexion.commit()
        except IndexError:
            return []
        
        return desencriptar_array(data)

    def obtener_datos_chat_privado(self, amigo1: str, amigo2: str):
        amigo1 = encriptar(amigo1)
        amigo2 = encriptar(amigo2)
        
        conexion = sqlite3.connect(self.database)

        cursor = conexion.cursor()
        cursor.execute(f"""SELECT rowid, * FROM chats_privados WHERE (amigo1 = '{amigo1}' AND amigo2 = '{amigo2}') 
                                                                  OR (amigo2 = '{amigo1}' AND amigo1 = '{amigo2}') """)
        
        try:
            data = cursor.fetchall()[0]
        
            conexion.commit()
        except IndexError:
            return []
        
        return desencriptar_array(data)
    
    
    def existe_el_chat_privado(self, amigo1: str, amigo2: str):
        datos_chat = self.obtener_datos_chat_privado(amigo1, amigo2)
        
        return (
            datos_chat[1] == amigo1 and datos_chat[2] == amigo2
            ) or (datos_chat[2] == amigo1 and datos_chat[1] == amigo2)
        
    def es_su_chat_privado_por_id(self, nombre: str, chat_privado_id: int):
        datos_chat = self.obtener_datos_chat_privado_por_id(chat_privado_id)
        
        return datos_chat[1] == nombre or datos_chat[2] == nombre




print(Gestionar_usuarios().listar_id_nombre_clave())

#Gestionar_chats_privados().crear_chat_privado('Fidel', 'Corvus')

id_chat = Gestionar_chats_privados().obtener_id_chat_privado('Corvus', 'Fidel')

#Gestionar_chats_privados().agregar_mensaje_chat_privado_por_id('Fidel', 'Después xdd', 'Hola Corvus :D !', id_chat)
#Gestionar_chats_privados().eliminar_mensaje_por_id('Fidel', 3, 1)

chat_privado = Gestionar_chats_privados().obtener_mensajes_chat_privado_por_id(id_chat)

print(chat_privado)

