# -*- coding: latin-1 -*-
from flask import Flask, render_template, request, session
import sqlite3
import scipy

#----------------------------------
# VARIÁVIES GLOBAIS
#----------------------------------
app = Flask(__name__)
tbl_usuarios = 'usuarios'
app.config['SECRET_KEY'] = "A0Zr98j/3yX R~XHH!jmN]/*-+hsHASHsh6 #$$"

#----------------------------------
# ROTAS
#----------------------------------
@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/registro", methods=['POST', 'GET'])
def registro():
    if(request.method == 'GET'):
        return render_template("registro.html")
    elif(request.method == 'POST'):
        _nome = request.form.get('nome')
        _email = request.form.get('email')
        _senha = request.form.get('pass')
        if(novo_usuario(_nome, _email, _senha)):
            return render_template("index.html", msg="Conta criada com sucesso!", type='success')
        else:
            return render_template("index.html", msg="Erro ao criar conta!", type='danger')

@app.route("/login", methods=['POST', 'GET'])
def efetuaLogin():
    if(request.method == 'GET'):
        return render_template("login.html")
    elif(request.method == 'POST'):
        _email = request.form.get('email')
        _senha = request.form.get('pass')
        if(valida_login(_email, _senha)):
            return render_template("minha-pagina.html")
        else:
            return render_template("index.html", msg='Email ou senha inválidos!', type='danger')

@app.route("/logout")
def logout():
    session.pop('usr_id', None)
    session.pop('usr_nome', None)
    session.pop('usr_email', None)
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

#----------------------------------
# MÉTODOS DO BANCO
#----------------------------------

# Método para efetuar login
def valida_login(_email, _senha):
    try:
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(''' SELECT * FROM usuarios WHERE email = ? AND senha = ?''', (_email, _senha))
        connect.commit()
        result = scipy.array(cursor.fetchall())
        for usuario in result:
            if(usuario[2] == ''):
                return False;
            session['usr_id'] = usuario[0]
            session['usr_email'] = usuario[1]
            session['usr_nome'] = usuario[2]
            return True
        else:
            return False
    except Exception as e:
        print ('valida_login(): ', e)
        return False
    print (_email)
    return False

# Método para criar um usuário
def novo_usuario(_nome, _email, _senha):
    try:
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('''INSERT INTO usuarios (nome, email, senha) VALUES (?,?,?)''', (_nome, _email, _senha))
        connect.commit()
        connect.close()
        return True
    except Exception as e:
        print ('novo_usuario(): ', e)
        return False

#----------------------------------
# MÉTODOS
#----------------------------------


if __name__ == "__main__":
    app.run(debug=True)
