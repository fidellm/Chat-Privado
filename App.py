import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, session, url_for, flash
from datetime import datetime
import gestionar_database as gs
import random


def crear_secret_key(caracteres: int):
    retornar = ""
    
    contador = 0
    
    while contador <= caracteres:
        caracter = random.choice(("a", "b", "c", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ñ", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"))
        
        probabilidad = random.randint(1, 100)

        if probabilidad <= 45:
            caracter = caracter.upper()
        
        contador = contador + 1
        
        retornar = retornar + caracter
        
    return retornar
    
#secret_key = crear_secret_key(6)
secret_key = "fideoscontuco123"

print("SECRET KEY = " + secret_key)

print("")

app = Flask (__name__)
app.secret_key = os.getenv("SECRET", secret_key)
""" Secret key changed to an environment variable. Helps generate session ID """


messages = []

clave_super_secreta = "amigos1234"

array_admins = {"alpha": "arrozfilo27", "corvus": "1920", "delta": "nacho1234"}

lista_usuarios_registrados = []

lista_usuarios_en_el_chat_public = []
usuarios_bloqueados_del_chat_public = []

def quitar_usuario_lista_en_chat_public(name: str):
    contador = 0
    
    for i in lista_usuarios_en_el_chat_public:
        #print(i)
        #print(i['name'])
        if i['name'] == name:
            lista_usuarios_en_el_chat_public.pop(contador)
            
        contador += 1
            

def agregar_usuario_lista_en_chat_public(name: str, is_admin: bool):
    gestionar = gs.Gestionar_usuarios()
    
    quitar_usuario_lista_en_chat_public(name= name)
    
    
    lista_usuarios_en_el_chat_public.append( { 'id': gestionar.obtener_id_por_nombre(nombre= name), 'name': name, 'is_admin': is_admin} )
    
    
    

def saber_si_se_parece_admin(nombre):
    for i in array_admins:
        if nombre.lower() in i.lower():
            return True
    return False

def saber_si_es_admin(name: str, password: str):
    for i in array_admins:
        if i.lower() == name.lower() and array_admins[i] == password:
            return True
    
    return False

def actualizar_ultima_conexion_usuario(username: str, ultima_conexion = None):
    gestionar = gs.Gestionar_usuarios()
    
    print("ESTE ESSS EL NOMBRE DE USUARIOOOO ===== " + username)
    if username.lower() in array_admins:
        return
    
    if ultima_conexion == None:
        now = get_time_now()
    else:
        now = ultima_conexion
    gestionar.actualizar_ultima_conexion(nombre=username, ultima_conexion=now)

def get_time_now():
    return datetime.now().strftime("%H:%M:%S")

def add_message(username, message, is_management_server: bool = False):
    """ Add messages to the 'messages' list """
    """ 1st set of {} refers to 1st argument = username """
    """ 2nd set of {} refers to 2nd argument = message """
    """ Python can accept either {1} or {} """
    if message.replace(" ", "") != "":
        now = get_time_now() # new variable = now

        if not is_management_server:
            actualizar_ultima_conexion_usuario(username=username)

        new_message = {"id_message": len(messages)+1, "timestamp": now, "from": username, "message":message, "visible": True}
        
        messages.append(new_message)
        return new_message



@app.route('/', methods = ["GET", "POST"]) # route decorator that aligns to index.html
def Index():
    try:
        username = session['username']
        user_password = session['user_password']
        
        
    except:
        return redirect(url_for('clean_user'))
    
    quitar_usuario_lista_en_chat_public(username)
    
    
    session['go_chat'] = False
    
    """ Main page with instructions """
    try:
        if session['remember_me']:
            return redirect(url_for('user_page'))
    except:
        session['remember_me'] = False

    
    if request.method == "POST":
        gestionar = gs.Gestionar_usuarios()
    
        session["username"] = str(request.form["username"])
        session["user_password"] = request.form["user_password"]
        
        username = session["username"]
        user_password = session["user_password"]
        
        
        try:
            if request.form["remember"] == 'on':
                session['remember_me'] = True
        except:
            session['remember_me'] = False
        
        if saber_si_es_admin(name= username, password= user_password):
            print("si es admin")
            username = session["username"]
            session["server_password"] = clave_super_secreta

            return redirect(url_for("user_page"))
        elif saber_si_se_parece_admin(username):
            flash(f"El nombre '{username}' está reservado para el administrador.")
        elif request.form["username"].replace(" ", "") == "":
            pass
        elif not gestionar.existe_el_usuario(nombre=username):
            flash("El usuario '" + request.form["username"] + "' no existe")
        elif request.form["server_password"] == clave_super_secreta and username.replace(" ", "") != "":
            if gestionar.es_el_usuario(nombre=username, clave=user_password):
                session["user_password"] = user_password
                session["server_password"] = clave_super_secreta

                return redirect(url_for("user_page"))
            else:
                session["username"] = ""
                session["user_password"] = ""
                session["server_password"] = ""
                flash("Esa no es la contraseña del usuario.")
        elif request.form["server_password"] != clave_super_secreta:
            flash("Esa no es la clave super secreta.")
        else:
            flash('Hubo un error :/')
            return redirect(url_for('clean_user'))
        
    
    return render_template("login.html")

@app.route('/register', methods = ["GET", "POST"])
def register():
    session['remember_me'] = False
    session['go_chat'] = False
    
    try:
        quitar_usuario_lista_en_chat_public(session['username'])
    except:
        pass
    
    if request.method == "POST":
        username = request.form["username"]
        user_password = request.form["user_password"]
        ultima_conexion = get_time_now()
        
        try:
            server_password = request.form["server_password"]
        except:
            server_password = ""
        
        try:
            if request.form["remember"] == 'on':
                session['remember_me'] = True
        except:
            session['remember_me'] = False
        
        
        gestionar = gs.Gestionar_usuarios()
        
        if username.replace(" ", "") == "" or username.replace(" ", "") != username:
            flash("El nombre debe tener letras y no tener ningún espacio")
        elif user_password == "":
            flash("Debes poner una contraseña para el usuario")
        elif len(username) > 10:
            flash("El nombre de usuario debe tener como máximo 10 caracteres")
        elif len(username) < 4:
            flash("El nombre debe tener como mínimo 4 caracteres")
        elif not server_password == clave_super_secreta:
            flash('Esa no es la contraseña de acceso al servidor...')
        elif saber_si_se_parece_admin(username):
            flash(f"El nombre '{username}' está reservado para el administrador")
        elif gestionar.existe_el_usuario(nombre=username):
            flash("El usuario '" + username + "' ya está registrado")
        else:
            gestionar.agregar_usuario(nombre=username, clave=user_password, primera_conexion=ultima_conexion, ultima_conexion=ultima_conexion)
            lista_usuarios_registrados.append(username)
            
            if session['remember_me']:
                session['username'] = username
                session['user_password'] = user_password
                flash('Bienvenido a La Red...')
                return redirect(url_for('user_page'))
            else:
                flash("Se agregó exitosamente el usuario!")
            
            return redirect(url_for('Index'))
    
    return render_template("register.html")

@app.route('/clean_user')
def clean_user():
    try:
        quitar_usuario_lista_en_chat_public(session['username'])
    except:
        pass
    
    session['username'] = ''
    session['user_password'] = ''
    session['remember_me'] = False
    session['go_chat'] = False
    
    return redirect(url_for('Index'))


@app.route('/user_page')
def user_page():
    try:
        username = session["username"]
        user_password = session['user_password']
        
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        es_admin = saber_si_es_admin(name=username, password=user_password)
        
        gestionar_usuarios = gs.Gestionar_usuarios()
        
        if username == "":
            print(f"\nEl nombre del usuario '{username}' que intentó entrar a '/user_page' ESTÁ VACÍO!\n")
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif user_password == "":
            print(f"\nLa contraseña del usuario '{username}' que intentó entrar a '/user_page' ESTÁ VACÍA!\n")
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif es_admin:
            pass
        elif not gestionar_usuarios.existe_el_usuario(nombre=username):
            print(f"EL USUARIO '{username}' QUE INTENTÓ ENTRAR A /user_page NO EXISTE")
            return redirect(url_for('clean_user'))
        elif not gestionar_usuarios.es_el_usuario(nombre=username, clave=user_password):
            print(f"EL USUARIO '{username}' NO TIENE LA CONTRASEÑA CORRECTA!")
            return redirect(url_for('clean_user'))
        
    except:
        print(session)
        print("hubo un error")
        flash("Intentaste entrar al menú de usuario sin iniciar sesion.")
        return redirect(url_for("clean_user"))
    
    session["go_chat"] = False
    quitar_usuario_lista_en_chat_public(username)
    
    
    if es_admin:
        print(f"El usuario ROOT '{username}' ingresó a /user_page")
    else:
        print(f'El usuario {username} ingresó a /user_page')
        
        
    return render_template("menu_user.html", username= username, title= 'Menú de usuario')

@app.route('/user_page/friends')
def menu_friends():
    try:
        username = session["username"]
        user_password = session['user_password']
        
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        es_admin = saber_si_es_admin(name=username, password=user_password)
        
        gestionar_usuarios = gs.Gestionar_usuarios()
        
        if username == "":
            print("EL NOMBRE DE USUARIO QUE INTENTÓ ENTRAR A /user_page/friends ESTÁ VACÍO!")
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif user_password == "":
            print("LA CONTRASEÑA QUE INTENTÓ ENTRAR A /user_page/friends ESTÁ VACÍO!")
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif es_admin:
            pass
        elif not gestionar_usuarios.existe_el_usuario(nombre=username):
            print(f"EL USUARIO '{username}' QUE INTENTÓ ENTRAR A /user_page/friends NO EXISTE")
            return redirect(url_for('clean_user'))
        elif not gestionar_usuarios.es_el_usuario(nombre=username, clave=user_password):
            print(f"EL USUARIO '{username}' NO TIENE LA CONTRASEÑA CORRECTA!")
            return redirect(url_for('clean_user'))
        
    except:
        print(session)
        print("hubo un error")
        flash("Intentaste entrar al menú de usuario sin iniciar sesion.")
        return redirect(url_for("clean_user"))
    
    gestionar_amigos = gs.Gestionar_Amigos()
    
    session['go_chat'] = False
    quitar_usuario_lista_en_chat_public(username)
    
    if es_admin:
        print(f"El usuario ROOT '{username}' ingresó a /user_page/menu_friends")
    else:
        print(f'El usuario {username} ingresó a /user_page/menu_friends')
    
    lista_amistades = gestionar_amigos.listar_amistades_de_un_usuario(username)
    lista_solicitudes_hacia_mi = gestionar_amigos.listar_solicitudes_hacia_un_usuario(nombre= username)
    
    return render_template('menu_friends.html', username = username, is_admin = es_admin, friends_list = lista_amistades, number_of_requests_for_me = len(lista_solicitudes_hacia_mi))

@app.route('/user_page/friends/delete_friend<int:friend_id>')
def delete_friend(friend_id):
    try:
        username = session["username"]
        user_password = session['user_password']
        
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        es_admin = saber_si_es_admin(name=username, password=user_password)
        
        gestionar_usuarios = gs.Gestionar_usuarios()
        
        if username == "":
            print("EL NOMBRE DE USUARIO QUE INTENTÓ ENTRAR A /user_page/friends ESTÁ VACÍO!")
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif user_password == "":
            print("LA CONTRASEÑA QUE INTENTÓ ENTRAR A /user_page/friends ESTÁ VACÍO!")
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif es_admin:
            pass
        elif not gestionar_usuarios.existe_el_usuario(nombre=username):
            print(f"EL USUARIO '{username}' QUE INTENTÓ ENTRAR A /user_page/friends NO EXISTE")
            return redirect(url_for('clean_user'))
        elif not gestionar_usuarios.es_el_usuario(nombre=username, clave=user_password):
            print(f"EL USUARIO '{username}' NO TIENE LA CONTRASEÑA CORRECTA!")
            return redirect(url_for('clean_user'))
        
    except:
        print(session)
        print("hubo un error")
        flash("Intentaste entrar al menú de usuario sin iniciar sesion.")
        return redirect(url_for("clean_user"))
    
    gestionar_amigos = gs.Gestionar_Amigos()
    if gestionar_amigos.es_su_amigo_por_id(amigo= username, id= friend_id):
        lista_amistad = gestionar_amigos.obtener_solicitud_o_amistad_por_id(id)
        if lista_amistad[1] == username:
            friend_name = lista_amistad[2]
        else:
            friend_name = lista_amistad[1]
        
        gestionar_amigos.eliminar_solicitud_o_amistad_por_id(id= friend_id)
        
        flash(f'Amigo {friend_name} eliminado exitosamente...')
    
    return redirect(url_for('menu_friends'))


@app.route('/user_page/friends/requests/send', methods= ["GET", "POST"])
def send_friend_request():
    try:
        username = session["username"]
        user_password = session['user_password']
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        es_admin = saber_si_es_admin(name=username, password=user_password)
        
        gestionar_usuarios = gs.Gestionar_usuarios()
        
        if username == "":
            print("EL NOMBRE DE USUARIO QUE INTENTÓ ENTRAR A /user_page/friends ESTÁ VACÍO!")
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif user_password == "":
            print("LA CONTRASEÑA QUE INTENTÓ ENTRAR A /user_page/friends ESTÁ VACÍO!")
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif es_admin:
            pass
        elif not gestionar_usuarios.existe_el_usuario(nombre=username):
            print(f"EL USUARIO '{username}' QUE INTENTÓ ENTRAR A /user_page/friends NO EXISTE")
            return redirect(url_for('clean_user'))
        elif not gestionar_usuarios.es_el_usuario(nombre=username, clave=user_password):
            print(f"EL USUARIO '{username}' NO TIENE LA CONTRASEÑA CORRECTA!")
            return redirect(url_for('clean_user'))
        
    except:
        print(session)
        print("hubo un error")
        flash("Intentaste entrar al menú de usuario sin iniciar sesion.")
        return redirect(url_for("clean_user"))
    
    
    if request.method == "POST":
        try:
            friend_username = request.form['friend_name']
        except:
            flash('Debes que ingresar el nombre del usuario para mandarle una solicitud de amistad')
            return redirect(url_for('menu_friends'))
        
        if friend_username.lower() in array_admins:
            pass
        else:
            try:
                if not gestionar_usuarios.es_el_usuario(nombre= friend_username, clave= gestionar_usuarios.pedir_clave_por_nombre(friend_username)):
                    flash(f'El usuario {friend_username} no existe...')
                    return redirect(url_for('menu_friends'))
            except IndexError:
                flash(f'El usuario {friend_username} no existe...')
                return redirect(url_for('menu_friends'))
    
        gestionar_amigos = gs.Gestionar_Amigos()
        
        if gestionar_amigos.es_su_amigo(amigo1= username, amigo2= friend_username): # Si ya eran amigos
            flash(f'El usuario {friend_username} ya es tu amigo...')
        elif gestionar_amigos.es_la_solicitud_hacia_el(amigo1= friend_username, amigo2= username): # Si el otro usuario ya le había enviado una solicitud
            flash(f'El usuario {friend_username} ya te había mandado una solicitud de amistad...')
        elif gestionar_amigos.es_su_amigo_o_solicitud(amigo1= username, amigo2= friend_username): # Si ya le había mandado una solicitud de amistad anteriormente
            flash(f'Ya has mandado una solicitud de amistad a {friend_username} anteriormente...')
        else:
            gestionar_amigos.mandar_solicitud_de_amistad(amigo1= username, amigo2= friend_username) # Manda la solicitud de amistad
            flash(f'Solicitud de amistad enviada con éxito a {friend_username}')

        return redirect(url_for('menu_friends')) # Regresa al menú de amigos

@app.route('/user_page/friends/requests') # Apartado de solicitudes de amistad
def friend_requests():
    try:
        username = session["username"]
        user_password = session['user_password']
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        es_admin = saber_si_es_admin(name=username, password=user_password)
        
        gestionar_usuarios = gs.Gestionar_usuarios()
        
        if username == "":
            print("EL NOMBRE DE USUARIO QUE INTENTÓ ENTRAR A /user_page/friends/requests ESTÁ VACÍO!")
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif user_password == "":
            print("LA CONTRASEÑA QUE INTENTÓ ENTRAR A /user_page/friends/requests ESTÁ VACÍO!")
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif es_admin:
            pass
        elif not gestionar_usuarios.existe_el_usuario(nombre=username):
            print(f"EL USUARIO '{username}' QUE INTENTÓ ENTRAR A /user_page/friends/requests NO EXISTE")
            return redirect(url_for('clean_user'))
        elif not gestionar_usuarios.es_el_usuario(nombre=username, clave=user_password):
            print(f"EL USUARIO '{username}' NO TIENE LA CONTRASEÑA CORRECTA!")
            return redirect(url_for('clean_user'))
        
    except:
        print(session)
        print("hubo un error")
        flash("Intentaste entrar al menú de usuario sin iniciar sesion.")
        return redirect(url_for("clean_user"))
    
    gestionar_amigos = gs.Gestionar_Amigos()
    
    solicitudes_hacia_el_usuario = gestionar_amigos.listar_solicitudes_hacia_un_usuario(nombre= username)
    solicitudes_del_usuario = gestionar_amigos.listar_solicitudes_de_un_usuario(nombre= username)
    #print(solicitudes_del_usuario)
    
    return render_template('friend_requests.html', username = username, is_admin = es_admin, requests_to_user = solicitudes_hacia_el_usuario, requests_from_user = solicitudes_del_usuario)

@app.route('/user_page/friends/requests/accept<int:request_id>') # Aceptar una solicitud de amistad
def accept_friend_request(request_id: int):
    try:
        username = session["username"]
        user_password = session['user_password']
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        es_admin = saber_si_es_admin(name=username, password=user_password)
        
        gestionar_usuarios = gs.Gestionar_usuarios()
        
        if username == "":
            print("EL NOMBRE DE USUARIO QUE INTENTÓ ENTRAR A /user_page/friends/requests/accept ESTÁ VACÍO!")
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif user_password == "":
            print("LA CONTRASEÑA QUE INTENTÓ ENTRAR A /user_page/friends/requests/accept ESTÁ VACÍO!")
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif es_admin:
            pass
        elif not gestionar_usuarios.existe_el_usuario(nombre=username):
            print(f"EL USUARIO '{username}' QUE INTENTÓ ENTRAR A /user_page/friends/requests/accept NO EXISTE")
            return redirect(url_for('clean_user'))
        elif not gestionar_usuarios.es_el_usuario(nombre=username, clave=user_password):
            print(f"EL USUARIO '{username}' NO TIENE LA CONTRASEÑA CORRECTA!")
            return redirect(url_for('clean_user'))
        
    except:
        print(session)
        print("hubo un error")
        flash("Intentaste entrar al menú de usuario sin iniciar sesion.")
        return redirect(url_for("clean_user"))
    
    gestionar_amigos = gs.Gestionar_Amigos()
    
    if (
        gestionar_amigos.es_la_solicitud_para_el(amigo2= username, id= request_id) 
        and not gestionar_amigos.es_su_amigo_por_id(amigo= username, id= request_id)
       ) and gestionar_amigos.es_su_amigo_o_solicitud_por_id(amigo= username, id= request_id) :
        
        friend_username = gestionar_amigos.obtener_solicitud_o_amistad_por_id(id= request_id)[1]
        
        time_now = get_time_now()
        
        gestionar_amigos.aceptar_solicitud(amigo1= friend_username, amigo2= username, fecha_amistad=time_now)
        flash(f'Solicitud de amistad aceptada a {friend_username} exitosamente...')
        
    else:
        flash(f'Ese usuario no te mandó una solicitud de amistad...')
    
    return redirect(url_for('friend_requests'))

@app.route('/user_page/friends/requests/from_me/cancel<int:friend_id>') #Cancelar solicitud de amistad enviada
def cancel_friend_request_from_me(friend_id: int):
    try:
        username = session["username"]
        user_password = session['user_password']
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        es_admin = saber_si_es_admin(name=username, password=user_password)
        
        gestionar_usuarios = gs.Gestionar_usuarios()
        
        if username == "":
            print("EL NOMBRE DE USUARIO QUE INTENTÓ ENTRAR A /user_page/friends/requests ESTÁ VACÍO!")
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif user_password == "":
            print("LA CONTRASEÑA QUE INTENTÓ ENTRAR A /user_page/friends/requests ESTÁ VACÍO!")
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif es_admin:
            pass
        elif not gestionar_usuarios.existe_el_usuario(nombre=username):
            print(f"EL USUARIO '{username}' QUE INTENTÓ ENTRAR A /user_page/friends/requests NO EXISTE")
            return redirect(url_for('clean_user'))
        elif not gestionar_usuarios.es_el_usuario(nombre=username, clave=user_password):
            print(f"EL USUARIO '{username}' NO TIENE LA CONTRASEÑA CORRECTA!")
            return redirect(url_for('clean_user'))
        
    except:
        print(session)
        print("hubo un error")
        flash("Intentaste entrar al menú de usuario sin iniciar sesion.")
        return redirect(url_for("clean_user"))
    
    gestionar_amigos = gs.Gestionar_Amigos()
    
    if gestionar_amigos.es_su_solicitud_por_id(amigo1= username, id= friend_id):
        friend_username = gestionar_amigos.obtener_solicitud_o_amistad_por_id(id= friend_id)[2]
        gestionar_amigos.cancelar_solicitud_de_amistad_por_id(amigo1= username, id= friend_id)
        flash(f'Solicitud de amistad a {friend_username} cancelada exitosamente...')
    else:
        flash('¿...? Esa solicitud no la has mandado, no debes cancelarla...')
    
    
    return redirect(url_for('friend_requests'))

@app.route('/user_page/logout')
def logout():
    try:
        gestionar = gs.Gestionar_usuarios()
        
        username = session["username"]
        try:
            user_password = session['user_password']
        except:
            print(f'El usuario {username} no tenía contraseña en la sesión')
        
        
        if username == "":
            print("el username está vacio")
            flash("Intentaste entrar al menú de usuario sin iniciar sesion.")
            return redirect(url_for("Index"))
        elif saber_si_es_admin(name=username, password=user_password):
            pass
        elif not gestionar.es_el_usuario(nombre=username, clave=user_password):
            print('Intentaste ingresar con un nombre de usuario que no existe')
        
        return redirect(url_for('clean_user'))
    except:
        return redirect(url_for("Index"))
    

@app.route('/chat/public/go', methods = ["GET", "POST"])
def go_chat():
    
    try:
        username = session["username"]
        user_password = session["user_password"]
        
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        gestionar = gs.Gestionar_usuarios()
        
        es_admin = saber_si_es_admin(name= username, password= user_password)
    
        if username == "":
            flash("No iniciaste sesión")
            return redirect(url_for("clean_user"))
        elif user_password == "":
            flash("No ingresaste una contraseña... ¿...?")
            return redirect(url_for('clean_user'))
        elif es_admin:
            pass
        elif not gestionar.es_el_usuario(nombre=username, clave=user_password):
            flash(f"Intentaste infiltrarte al servidor con un usuario falso. No lo vuelvas a intentar...")
            print(f"Alguien quiso infiltrarse con el nombre de usuario '{username}'")
            return redirect(url_for("clean_user"))
    except:
        flash("No has iniciado una sesión...")
        return redirect(url_for("clean_user"))
    
    if not saber_si_es_admin(name=username, password=user_password):
        print("no es admin xd")
        gestionar.actualizar_ultima_conexion(username, get_time_now())
    
    session["go_chat"] = True
    
    agregar_usuario_lista_en_chat_public(name= username, is_admin= es_admin)
    
    add_message("Gestión del servidor", "'" + username + "'" + " se ha unido", True)

    return redirect(url_for("chat_public"))


@app.route('/chat/public', methods = ["GET", "POST"])
def chat_public():
    """ Add & Display chat messages. {0} = username argument """
    """ username & messages get added to the list """

    try:
        username = session["username"]
        user_password = session["user_password"]
        
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        es_admin = saber_si_es_admin(name= username, password= user_password)
        
        gestionar = gs.Gestionar_usuarios()
        
        if username == "":
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif user_password == "":
            flash("No ingresaste una contraseña... ¿...?")
            return redirect(url_for('clean_user'))
        elif es_admin:
            pass
        elif not gestionar.es_el_usuario(nombre=username, clave=user_password):
            flash("No iniciaste sesión y además quisiste infiltrarte con un usuario falso...")
            print(f"Alguien quiso infiltrarse con el nombre de usuario '{username}'")
            return redirect(url_for("clean_user"))
        elif not session["go_chat"]:
            return redirect(url_for("user_page"))
    except:
        flash("No has iniciado una sesión...")
        return redirect(url_for("clean_user"))
    
    try:
        message = request.form['message']
    except:
        pass
    
    
    agregar_usuario_lista_en_chat_public(name= username, is_admin= es_admin)
    
    #quitar_usuario_lista_online_en_chat_public(username)
    #print(lista_usuarios_en_el_chat_public)
    
    
    if request.method == "POST":
        add_message(username=username, message=message)
        #print(messages)
        return redirect(url_for('chat_public'))
    
    
    return render_template("chat_user.html", username = username, is_admin = es_admin, messages = messages[::-1], users_in_chat_public = lista_usuarios_en_el_chat_public, title= 'Chat público', url_chat_delete = '/chat/public/delete', url_message_delete= '/chat/public/delete/')


@app.route('/chat/public/delete')
def delete_chat_public():
    try:
        username = session["username"]
        user_password = session["user_password"]
        
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        gestionar = gs.Gestionar_usuarios()
        
        es_admin = saber_si_es_admin(name= username, password= user_password)
        
        if not es_admin:
            if username == "":
                print(f"ALGUIEN INTENTÓ BORRAR UN MENSAJE DEL CHAT PÚBLICO SIN INICIAR SESIÓN")
                flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste borrar el chat público...")
                return redirect(url_for("Index"))
            elif user_password == '':
                print(F"EL USUARIO '{username}' INTENTÓ BORRAR EL CHAT PÚBLICO SIN UNA CONTRASEÑA")
                flash(f"¿Qué intentaste hacer? No iniciaste sesión con contraseña, no sos administrador, e intentaste borrar el chat público...")
            elif not gestionar.es_el_usuario(nombre= username, clave= user_password):
                print(f"\nEl usuario {username} intentó borrar el chat público con una contraseña falsa...\n")
                flash("Intentaste borrar el chat público con un usuario falso... No lo vuelvas a intentar...")
                return redirect(url_for('clean_user'))
            
            print(f"UN USUARIO NORMAL '{username}' INTENTÓ BORRAR EL CHAT PÚBLICO")
            flash("¿Qué intentaste hacer? No sos administrador e intentaste borrar el chat público...")

        
    except:
        flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste borrar el chat público...")
        return redirect(url_for("clean_user"))
    
    global messages
    messages = []
    
    return redirect(url_for("chat_public"))

@app.route('/chat/public/delete/<int:id_message>')
def delete_message_chat_public(id_message: int):
    try:
        username = session["username"]
        user_password = session["user_password"]
        
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        gestionar = gs.Gestionar_usuarios()
        
        es_admin = saber_si_es_admin(name= username, password= user_password)
        
        if not es_admin:
            if username == "":
                print(f"ALGUIEN INTENTÓ BORRAR UN MENSAJE DEL CHAT PÚBLICO SIN INICIAR SESIÓN")
                flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste borrar el chat público...")
                return redirect(url_for("Index"))
            elif user_password == '':
                print(F"EL USUARIO '{username}' INTENTÓ BORRAR EL CHAT PÚBLICO SIN UNA CONTRASEÑA")
                flash(f"¿Qué intentaste hacer? No iniciaste sesión con contraseña, no sos administrador, e intentaste borrar el chat público...")
            elif not gestionar.es_el_usuario(nombre= username, clave= user_password):
                print(f"\nEl usuario {username} intentó borrar el chat público con una contraseña falsa...\n")
                flash("Intentaste borrar el chat público con un usuario falso... No lo vuelvas a intentar...")
                return redirect(url_for('clean_user'))
            
        
    except:
        flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste borrar el chat público...")
        return redirect(url_for("clean_user"))
    
    contador = 0
    if es_admin:
        for i in messages:
            if i['id_message'] == id_message:
                messages.pop(contador)
            contador += 1
    else:
        for i in messages:
            if i['id_message'] == id_message:
                messages[contador]['visible'] = False
            contador += 1
    
    
    return redirect(url_for("chat_public"))



@app.route('/chat/private/menu/<string:saber_crear_chat>')
def menu_private_chats(saber_crear_chat: str = 'no'):
    try:
        username = session["username"]
        user_password = session["user_password"]
        
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        es_admin = saber_si_es_admin(name= username, password= user_password)
        
        gestionar = gs.Gestionar_usuarios()
        
        if username == "":
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif user_password == "":
            flash("No ingresaste una contraseña... ¿...?")
            return redirect(url_for('clean_user'))
        elif es_admin:
            pass
        elif not gestionar.es_el_usuario(nombre=username, clave=user_password):
            flash("No iniciaste sesión y además quisiste infiltrarte con un usuario falso...")
            print(f"Alguien quiso infiltrarse con el nombre de usuario '{username}'")
            return redirect(url_for("clean_user"))
#        elif not session["go_chat"]:
#            return redirect(url_for("user_page"))
    except:
        flash("No has iniciado una sesión...")
        return redirect(url_for("clean_user"))
    
    gestionar_amigos = gs.Gestionar_Amigos()
    
    lista_amistades = gestionar_amigos.listar_amistades_de_un_usuario(nombre= username)
    
    if 'yes' in saber_crear_chat:
        id_friend = int(saber_crear_chat.replace('yes', ''))
        return render_template('private_chats_menu.html', username= username, is_admin= es_admin, friends_list = lista_amistades, create_chat= [True, id_friend])
    elif saber_crear_chat == 'no':
        return render_template('private_chats_menu.html', username= username, is_admin= es_admin, friends_list = lista_amistades, create_chat= [False])

@app.route('/chat/private/<int:chat_private_id>', methods= ["GET", "POST"])
def chat_private(chat_private_id: int):
    try:
        username = session["username"]
        user_password = session["user_password"]
        
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        es_admin = saber_si_es_admin(name= username, password= user_password)
        
        gestionar = gs.Gestionar_usuarios()
        
        if username == "":
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif user_password == "":
            flash("No ingresaste una contraseña... ¿...?")
            return redirect(url_for('clean_user'))
        elif es_admin:
            pass
        elif not gestionar.es_el_usuario(nombre=username, clave=user_password):
            flash("No iniciaste sesión y además quisiste infiltrarte con un usuario falso...")
            print(f"Alguien quiso infiltrarse con el nombre de usuario '{username}'")
            return redirect(url_for("clean_user"))
#        elif not session["go_chat"]:
#            return redirect(url_for("user_page"))
    except:
        flash("No has iniciado una sesión...")
        return redirect(url_for("clean_user"))
    
    
    quitar_usuario_lista_en_chat_public(username)
    
    gestionar_chat_privado = gs.Gestionar_chats_privados()
    
    if not gestionar_chat_privado.es_su_chat_privado_por_id(nombre= username, chat_privado_id=chat_private_id):
        flash('Este no es tu chat...')
        return redirect(url_for('user_page'))
    
    try:
        message = request.form['message']
    except:
        pass
    
    
    
    mensajes_chat_privado = gestionar_chat_privado.obtener_mensajes_chat_privado_por_id(chat_id= chat_private_id)
    
    if request.method == "POST":
        mensaje = request.form['message']
        now = get_time_now()
        
        gestionar_chat_privado.agregar_mensaje_chat_privado_por_id(emisor= username, fecha_mensaje=now, mensaje= mensaje, chat_id= chat_private_id)
        
        return redirect(url_for('chat_private', chat_private_id= chat_private_id))
    
    
    return render_template("chat_user.html", username = username, is_admin = es_admin, messages = mensajes_chat_privado[::-1], users_in_chat_public = lista_usuarios_en_el_chat_public, title= 'Chat Privado', url_chat_delete = '/chat/private/delete', url_message_delete= '/chat/private/delete/')
    


@app.route('/manage_users')
def manage_users():
    try:
        username = session["username"]
        user_password = session["user_password"]
        
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        if not saber_si_es_admin(name = username, password = user_password):
            if username == "":
                flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste administrar los usuarios desde la base de datos...")
            else:
                flash("¿Qué intentaste hacer? No sos administrador e intentaste administrar los usuarios desde la base de datos...")
            
            return redirect(url_for("Index"))
    except:
        flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste borrar el chat público...")
        return redirect(url_for("clean_user"))
    
    gestionar_usuarios = gs.Gestionar_usuarios()
    
    lista_usuarios = gestionar_usuarios.listar_usuarios()
    lista_usuarios = lista_usuarios
    
    return render_template("manage_users.html", users = lista_usuarios)

@app.route('/manage_users/edit<int:id>')
def edit_user(id: int):
    try:
        gestionar = gs.Gestionar_usuarios()
        
        username = session["username"]
        user_password = session["user_password"]
        
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        
        if not saber_si_es_admin(name = username, password = user_password):
            if username == "":
                flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste administrar los usuarios de la base de datos...")
            else:
                flash("¿Qué intentaste hacer? No sos administrador e intentaste administrar los usuarios de la base de datos...")
            
            return redirect(url_for('clean_user'))
    except:
        flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste administrar los usuarios de la base de datos...")
        return redirect(url_for('clean_user'))
    
    
    return render_template("edit_user.html", user= gestionar.listar_id_nombre_clave_por_id(id= id))
    
@app.route('/manage_users/edit<int:id>/update', methods= ["POST"])
def update_user(id: int):
    try:
        gestionar = gs.Gestionar_usuarios()
        
        username = session["username"]
        user_password = session["user_password"]
        
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        
        if not saber_si_es_admin(name = username, password = user_password):
            if username == "":
                flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste administrar los usuarios de la base de datos...")
            else:
                flash("¿Qué intentaste hacer? No sos administrador e intentaste administrar los usuarios de la base de datos...")
            
            return redirect(url_for('clean_user'))
    except:
        flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste administrar los usuarios de la base de datos...")
        return redirect(url_for('clean_user'))
    
    if request.method == "POST":
        gestionar.actualizar_usuario(id= id, clave=request.form["password"])


@app.route('/manage_users/delete<int:id>')
def delete_user(id: int):
    try:
        gestionar_usuarios = gs.Gestionar_usuarios()
        
        username = session["username"]
        user_password = session["user_password"]
        
        try:
            if session['server_password'] != clave_super_secreta:
                flash('No has ingresado con la verdadera clave de acceso al servidor y sus funciones')
                return redirect(url_for('clean_user'))
        except:
            flash('No has ingresado con la clave de acceso al servidor y sus funciones...')
            return redirect(url_for('clean_user'))
        
        
        if not saber_si_es_admin(name = username, password = user_password):
            if username == "":
                flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste administrar los usuarios de la base de datos...")
            else:
                flash("¿Qué intentaste hacer? No sos administrador e intentaste administrar los usuarios de la base de datos...")
            
            return redirect(url_for('clean_user'))
    except:
        flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste administrar los usuarios de la base de datos...")
        return redirect(url_for('clean_user'))
    
    gestionar_usuarios.eliminar_usuario(id= id)
    
    return redirect(url_for('manage_users'))
    


print(clave_super_secreta +""" es la clave super secreta
""")


if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', '80')), debug=True)

