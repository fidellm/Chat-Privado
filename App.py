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

clave_super_secreta = "judnjota"

array_admins = {"alpha": "arrozfilo27", "corvus": "1920"}

lista_usuarios_en_el_chat_public = []
usuarios_bloqueados_del_chat_public = []

def quitar_usuario_lista_en_chat_public(name: str):
    contador = 0
    
    for i in lista_usuarios_en_el_chat_public:
        print(i)
        print(i['name'])
        if i['name'] == name:
            lista_usuarios_en_el_chat_public.pop(contador)
            
        contador += 1
            

def agregar_usuario_lista_en_chat_public(name: str, is_admin: bool):
    gestionar = gs.Gestionar_usuarios("DATABASE")
    
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
    gestionar = gs.Gestionar_usuarios("DATABASE")
    
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

        new_message = {"timestamp": now, "from": username, "message":message}
        
        messages.append(new_message)
        return new_message



@app.route('/', methods = ["GET", "POST"]) # route decorator that aligns to index.html
def Index():
    
    gestionar = gs.Gestionar_usuarios("DATABASE")
    
    try:
        username = session['username']
        user_password = session['user_password']
    except:
        username = ''
        user_password = ''
    
    quitar_usuario_lista_en_chat_public(username)
    
    if not gestionar.es_el_usuario(nombre=username, clave=user_password):
        session['username'] = ''
        session['user_password'] = ''
        session['remember_me'] = False
    
    session['go_chat'] = False
    
    """ Main page with instructions """
    try:
        if session['remember_me']:
            return redirect(url_for('user_page'))
    except:
        pass
    
    if request.method == "POST":
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
#            add_message("Gestión del servidor", "'" + session["username"] + "'" + " se ha unido")
            return redirect(url_for("user_page"))
        elif saber_si_se_parece_admin(username):
            flash(f"El nombre '{username}' está reservado para el administrador.")
        elif request.form["username"].replace(" ", "") == "":
            pass
        elif not gestionar.existe_el_usuario(nombre=username):
            flash("El usuario '" + request.form["username"] + "' no existe")
        elif request.form["server_password"] == clave_super_secreta and username.replace(" ", "") != "":
            if gestionar.es_el_usuario(nombre=username, clave=user_password):
                session["user_password"] = request.form["user_password"]
                session["server_password"] = request.form["server_password"]
#                add_message("Gestión del servidor", "'" + session["username"] + "'" + " se ha unido")
                return redirect(url_for("user_page"))
            else:
                session["username"] = ""
                session["user_password"] = ""
                session["server_password"] = ""
                flash("Esa no es la contraseña del usuario.")
        elif request.form["server_password"] != clave_super_secreta:
            flash("Esa no es la clave super secreta.")
            
        
#    if "username" in session and "clave_super_secreta" in session:
#        add_message("Gestión del servidor", "'" + session["username"] + "'" + " se ha unido")
#        return redirect(url_for("user", username=session["username"]))
    
    return render_template("login.html") # 'index.html' now replaces message

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
            if request.form["remember"] == 'on':
                session['remember_me'] = True
        except:
            session['remember_me'] = False
        
        
        gestionar = gs.Gestionar_usuarios("DATABASE")
        
        if username.replace(" ", "") == "" or username.replace(" ", "") != request.form["username"]:
            flash("El nombre debe tener letras y no tener ningún espacio")
        elif user_password == "":
            flash("Debes poner una contraseña para el usuario")
        elif len(username) > 10:
            flash("El nombre de usuario debe tener como máximo 10 caracteres")
        elif len(username) < 4:
            flash("El nombre debe tener como mínimo 4 caracteres")
        elif saber_si_se_parece_admin(username):
            flash("El nombre 'Alpha' está reservado para el administrador")
        elif gestionar.existe_el_usuario(nombre=username):
            flash("El usuario '" + username + "' ya está registrado")
        else:
            gestionar.agregar_usuario(nombre=username, clave=user_password, primera_conexion=ultima_conexion, ultima_conexion=ultima_conexion)
            
            if session['remember_me']:
                session['username'] = username
                session['user_password'] = user_password
                flash('Bienvenido a La Red...')
            else:
                flash("Se agregó exitosamente el usuario!")
            
            return redirect(url_for('Index'))
    
    return render_template("register.html")

@app.route('/clean_user')
def clean_user():
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
        
        es_admin = saber_si_es_admin(name=username, password=user_password)
        
        gestionar_usuarios = gs.Gestionar_usuarios("DATABASE")
        
        if username == "":
            print("EL NOMBRE DE USUARIO QUE INTENTÓ ENTRAR A /user_page ESTÁ VACÍO!")
            flash("No iniciaste sesión...")
            return redirect(url_for("clean_user"))
        elif user_password == "":
            print("LA CONTRASEÑA QUE INTENTÓ ENTRAR A /user_page ESTÁ VACÍO!")
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

@app.route('/user_page/logout')
def logout():
    try:
        gestionar = gs.Gestionar_usuarios('DATABASE')
        
        
        username = session["username"]
        try:
            user_password = session['user_password']
        except:
            print(f'El usuario {username} no tenía contraseña en la sesión')
        
        session['username'] = ''
        
        if username == "":
            print("el username está vacio")
            flash("Intentaste entrar al menú de usuario sin iniciar sesion.")
            return redirect(url_for("Index"))
        elif saber_si_es_admin(name=username, password=user_password):
            pass
        elif not gestionar.es_el_usuario(nombre=username, clave=user_password):
            print('Intentaste ingresar con un nombre de usuario que no existe')
        
        return redirect(url_for('Index'))
    except:
        print(session)
        print("hubo un error")
        flash("Intentaste cerrar sesión sin iniciar sesion.")
        return redirect(url_for("Index"))
    

@app.route('/chat/public/go', methods = ["GET", "POST"])
def go_chat():
    
    try:
        username = session["username"]
        user_password = session["user_password"]
        gestionar = gs.Gestionar_usuarios("DATABASE")
        
        es_admin = saber_si_es_admin(name= username, password= user_password)
    
        if username == "":
            flash("No iniciaste sesión")
            return redirect(url_for("clean_user"))
        elif es_admin:
            pass
        elif not gestionar.es_el_usuario(nombre=username, clave=user_password):
            flash(f"Intentaste infiltrarte al servidor con el nombre de usuario {username}. No lo vuelvas a intentar...")
            print(f"Alguien quiso infiltrarse con el nombre de usuario '{username}'")
            return redirect(url_for("clean_user"))
    except:
        return redirect(url_for("user_page"))
    
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
        
        es_admin = saber_si_es_admin(name= username, password= user_password)
        
        gestionar = gs.Gestionar_usuarios("DATABASE")
        
        if username == "":
            flash("No iniciaste sesión...")
            return redirect(url_for("Index"))
        elif es_admin:
            pass
        elif not gestionar.es_el_usuario(nombre=username, clave=user_password):
            flash("No iniciaste sesión y además quisiste infiltrarte con un nombre de usuario falso...")
            return redirect(url_for("Index"))
        elif not session["go_chat"]:
            return redirect(url_for("user_page"))
    except:
        return redirect(url_for("Index"))
    
    try:
        message = request.form['message']
    except:
        pass
    
    
    agregar_usuario_lista_en_chat_public(name= username, is_admin= es_admin)
    
    #quitar_usuario_lista_online_en_chat_public(username)
    print(lista_usuarios_en_el_chat_public)
    
    
    if request.method == "POST":
        add_message(username=username, message=message)
        print(messages)
        return redirect(url_for('chat_public'))
    
    
    return render_template("chat_user.html", username = username, is_admin = es_admin, messages = messages[::-1], users_in_chat_public = lista_usuarios_en_el_chat_public, title= 'Chat público')


@app.route('/chat/public/delete')
def delete_chat():
    try:
        username = session["username"]
        user_password = session["user_password"]
        
        if not saber_si_es_admin(name= username, password= user_password):
            if username == "":
                print(f"ALGUIEN INTENTÓ BORRAR EL CHAT PÚBLICO SIN INICIAR SESIÓN")
                flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste borrar el chat público...")
                return redirect(url_for("Index"))
            elif user_password == '':
                print(F"EL USUARIO '{username}' INTENTÓ BORRAR EL CHAT PÚBLICO SIN UNA CONTRASEÑA")
                flash(f"¿Qué intentaste hacer? No iniciaste sesión con contraseña, no sos administrador, e intentaste borrar el chat público...")
            
            print(f"UN USUARIO NORMAL INTENTÓ BORRAR EL CHAT PÚBLICO")
            flash("¿Qué intentaste hacer? No sos administrador e intentaste borrar el chat público...")
    except:
        flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste borrar el chat público...")
        return redirect(url_for("Index"))
    
    global messages
    messages = []
    
    return redirect(url_for("chat_public", username=session["username"]))



@app.route('/manage_users')
def manage_users():
    try:
        username = session["username"]
        user_password = session["user_password"]
        
        if not saber_si_es_admin(name = username, password = user_password):
            if username == "":
                flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste administrar los usuarios desde la base de datos...")
            else:
                flash("¿Qué intentaste hacer? No sos administrador e intentaste administrar los usuarios desde la base de datos...")
            
            return redirect(url_for("Index"))
    except:
        flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste borrar el chat público...")
        return redirect(url_for("Index"))
    
    gestionar_usuarios = gs.Gestionar_usuarios("DATABASE")
    
    lista_usuarios = gestionar_usuarios.listar_usuarios()
    lista_usuarios = gs.desencriptar_varios_arrays(lista_usuarios)
    
    return render_template("manage_users.html", users = lista_usuarios)

@app.route('/manage_users/delete<int:id>')
def delete_user(id: int):
    try:
        gestionar_usuarios = gs.Gestionar_usuarios("DATABASE")
        
        username = session["username"]
        user_password = session["user_password"]
        
        if not saber_si_es_admin(name = username, password = user_password):
            if username == "":
                flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste administrar los usuarios desde la base de datos...")
            else:
                flash("¿Qué intentaste hacer? No sos administrador e intentaste administrar los usuarios desde la base de datos...")
            
            return redirect(url_for('clean_user'))
    except:
        flash("¿Qué intentaste hacer? No iniciaste sesión, no sos administrador, e intentaste borrar el chat público...")
        return redirect(url_for('clean_user'))
    
    gestionar_usuarios.eliminar_usuario(id= id)
    
    return redirect(url_for('manage_users'))
    


print(clave_super_secreta +""" es la clave super secreta
""")


if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', '80')), debug=True)