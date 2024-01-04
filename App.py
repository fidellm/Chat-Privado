import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, session, url_for, flash
import time
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
    
secret_key = crear_secret_key(6)

print("SECRET KEY = " + secret_key)

print("")

app = Flask (__name__)
app.secret_key = os.getenv("SECRET", secret_key)
""" Secret key changed to an environment variable. Helps generate session ID """
messages = []

clave_super_secreta = "judnjota"

array_admins = {"Alpha": "arrozfilo27", "Corvus": "1920"}

def saber_si_se_parece_admin(nombre):
    for i in array_admins:
        if nombre.lower in i.lower():
            return True
    return False

def saber_si_es_admin(name: str, password: str):
    for i in array_admins:
        if i.lower() == name.lower() and array_admins[i] == password:
            return True
    
    return False
        

def get_time_now():
    return datetime.now().strftime("%H:%M:%S")

def add_message(username, message):
    """ Add messages to the 'messages' list """
    """ 1st set of {} refers to 1st argument = username """
    """ 2nd set of {} refers to 2nd argument = message """
    """ Python can accept either {1} or {} """
    if message != "" or message.replace(" ", "") != "":
        now = get_time_now() # new variable = now
    
        messages.append({"timestamp": now, "from": username, "message":message})


chat = messages

@app.route('/', methods = ["GET", "POST"]) # route decorator that aligns to index.html
def Index():
    """ Main page with instructions """
    if request.method == "POST":
        session["username"] = request.form["username"].title()
        session["user_password"] = request.form["user_password"]
        
        username = session["username"]
        user_password = session["user_password"]
        
        gestionar = gs.Gestionar_usuarios("DATABASE")
        
        if saber_si_es_admin(name= username, password= user_password):
            session["server_password"] = clave_super_secreta
#            add_message("Gestión del servidor", "'" + session["username"] + "'" + " se ha unido")
            return redirect(url_for("user_page"))
        elif saber_si_se_parece_admin(username):
            flash(f"El nombre '{username}' está reservado para el administrador.")
        elif request.form["username"].replace(" ", "") == "":
            pass
        elif not ((gs.encriptar(username), ) in gestionar.listar_nombres()):
            flash("El usuario '" + request.form["username"] + "' no existe")
        elif request.form["clave"] == clave_super_secreta and request.form["username"].replace(" ", "") != "":
            clave_verdadera = gestionar.pedir_clave_por_nombre(session["username"])
            if request.form["user_password"] == clave_verdadera:
                session["user_password"] = request.form["user_password"]
                session["server_password"] = request.form["server_password"]
#                add_message("Gestión del servidor", "'" + session["username"] + "'" + " se ha unido")
                return redirect(url_for("user_page"))
            else:
                flash("Esa no es la contraseña del usuario.")
        elif request.form["server_password"] != clave_super_secreta:
            flash("Esa no es la clave super secreta.")
            
        
#    if "username" in session and "clave_super_secreta" in session:
#        add_message("Gestión del servidor", "'" + session["username"] + "'" + " se ha unido")
#        return redirect(url_for("user", username=session["username"]))
    
    return render_template("login.html") # 'index.html' now replaces message

@app.route('/register', methods = ["GET", "POST"])
def register():
    
    
    if request.method == "POST":
        nombre = request.form["username"].lower()
        clave = request.form["user_password"]
        ultima_conexion = get_time_now()
        
        gestionar = gs.Gestionar_usuarios("DATABASE")
        
        if request.form["username"].replace(" ", "") == "" or request.form["username"].replace(" ", "") != request.form["username"]:
            flash("El nombre debe tener letras y no tener ningún espacio")
        elif clave == "":
            flash("Debes poner una contraseña para el usuario")
        elif len(request.form["username"]) > 10:
            flash("El nombre de usuario debe tener como máximo 10 caracteres")
        elif len(request.form["username"]) < 4:
            flash("El nombre debe tener como mínimo 4 caracteres")
        elif "alpha" in request.form["username"].lower():
            flash("El nombre 'Alpha' está reservado para el administrador")
        elif (gs.encriptar(request.form["username"]), ) in gestionar.listar_nombres():
            flash("El usuario '" + nombre + "' ya está registrado")
        else:
            gestionar.agregar_usuario(nombre, clave, ultima_conexion)
            flash("Se agregó exitosamente el usuario!")
            return redirect(url_for('Index'))
    
    return render_template("register.html")


@app.route('/user_page')
def user_page():
    try:
        username = session["username"]
        if username == "":
            return redirect(url_for("Index"))
    except:
        return redirect(url_for("Index"))
    
    return render_template("menu_user.html", username = username)


@app.route('/chat', methods = ["GET", "POST"])
def go_chat():    
    try:
        username = session["username"]
        if username == "":
            return redirect(url_for("Index"))
    except:
        return redirect(url_for("user_page"))
    
    add_message("Gestión del servidor", "'" + username + "'" + " se ha unido")

    return redirect(url_for("chat_public"))


@app.route('/chat/public/go', methods = ["GET", "POST"])
def chat_public():
    """ Add & Display chat messages. {0} = username argument """
    """ username & messages get added to the list """



    try:
        message = request.form["message"]
    except:
        message = ""
    
    try:
        username = session["username"]
        if username == "":
            return redirect(url_for("Index"))
    except:
        return redirect(url_for("Index"))
    
    if request.method == "POST":
        username = session["username"]
        message = request.form["message"]
        add_message(username,message)
        return redirect(url_for("user", username=session["username"]))

    if username != "Alpha":
        return render_template("chat.html", username = username, chat_messages = messages[::-1], mensaje = message)
    else:
        return render_template("chat_root.html", username = username, chat_messages = messages[::-1], mensaje = message)
        

@app.route('/chat/public/delete')
def delete_chat():
    try:
        if session["username"] == "" or not (saber_si_es_admin(name= session["username"], password= session["user_password"])):
            return redirect(url_for("Index"))
    except:
        return redirect(url_for("Index"))
    
    global messages
    messages = []
    
    return redirect(url_for("chat_public", username=session["username"]))
    

print(clave_super_secreta +""" es la clave super secreta
""")


if __name__ == '__main__':
    app.run(host=os.getenv('IP', "0.0.0.0"), port=int(os.getenv('PORT', "5000")), debug=True) # debug=False for production. 
    """ Fallback values for IP = 0.0.0.0 & PORT = 5000 """
