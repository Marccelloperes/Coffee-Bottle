# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session, url_for, jsonify
from functools import wraps
from Adafruit_IO import Client, Feed
import sqlite3
import db

#----------------------------------
# VARIÁVIES GLOBAIS
#----------------------------------
app = Flask(__name__)
tbl_usuarios = 'usuarios'
app.config['SECRET_KEY'] = "A0Zr98j/3yX R~XHH!jmN]/*-+hsHASHsh6 #$$"
ADAFRUIT_IO_KEY = 'dfee8fe53e5545398320b5119bd83de3'
ADAFRUIT_IO_USERNAME = 'eraldojr'
ocupada = False
adafruit = Client(ADAFRUIT_IO_KEY)

#----------------------------------
# ROTAS
#----------------------------------
@app.route("/")
def hello():
    return render_template("index.html"), 200

@app.route("/login", methods=['POST', 'GET'])
def efetuaLogin():
    if(session):
        return render_template("minha-pagina.html"), 200
    elif(request.method == 'GET'):
        return render_template("login.html"), 200
    elif(request.method == 'POST'):
        _email = request.form.get('email')
        _senha = request.form.get('pass')
        usuario = db.valida_login(_email, _senha)
        if usuario.size:
            print (usuario)
            session.permanent = True
            session['usr_id'] = usuario[0]
            session['usr_email'] = usuario[1]
            session['usr_nome'] = usuario[2]
            session['usr_tag'] = usuario[4]
            session['usr_nivel'] = usuario[5]
            session['usr_ativo'] = usuario[6]
            return render_template("minha-pagina.html"), 200
        else:
            return render_template("index.html", msg='Email ou senha inválidos!', type='danger'), 401

@app.route("/logout")
def logout():

    session.pop('_permanent', None)
    session.pop('usr_id', None)
    session.pop('usr_nome', None)
    session.pop('usr_email', None)
    session.pop('usr_tag', None)
    session.pop('usr_nivel', None)
    session.pop('usr_ativo', None)
    return render_template("index.html"), 200


@app.route("/minha-pagina", methods=['POST', 'GET'])
def minhaPagina():
    if session:
        return render_template("minha-pagina.html"), 200
    else:
        return render_template("erros/nao-logado.html"), 401

@app.route("/pedir-cafe")
def pedirCafe():
    if(session):
        if(db.busca_tag(session['usr_tag'])):
            return render_template("minha-pagina.html", msg="Solicitado. Seu café estará liberado por 30 segundos.", type='success'), 201
        else:
            return render_template("minha-pagina.html", msg="Erro! Você está autorizado?.", type='danger'), 401
    else:
        return render_template("erros/nao-logado.html"), 401

@app.route("/sobre")
def sobre():
    return render_template("sobre.html"), 200

@app.route("/registro", methods=['POST', 'GET'])
def registro():
    if(request.method == 'GET'):
        return render_template("registro.html"), 200
    elif(request.method == 'POST'):
        _nome = request.form.get('nome')
        _email = request.form.get('email')
        _senha = request.form.get('pass')
        if(db.novo_usuario(_nome, _email, _senha)):
            return render_template("index.html", msg="Conta criada com sucesso!", type='success'), 201
        else:
            return render_template("index.html", msg="Erro ao criar conta!", type='danger'), 500

@app.route("/gerenciar-usuarios")
def gerenciarUsuarios():
    if(session and session['usr_nivel'] == '1'):
        result = db.busca_usuarios()
        return render_template("gerenciar-usuarios.html", usuarios=result), 200
    else:
        result = db.busca_usuarios()
        return render_template("erros/nao-autorizado.html", usuarios=result), 401

@app.route("/historico")
def historico():
    return render_template("historico.html"), 200

@app.route("/ativar-usuario/<id>")
def ativarUsuario(id):
    if(db.ativar_usuario(id)):
        result = db.busca_usuarios()
        return render_template("gerenciar-usuarios.html",usuarios=result, msg="Alteração feita com sucesso!", type='success'), 200
    else:
        result = db.busca_usuarios()
        return render_template("gerenciar-usuarios.html", msg="Não foi possível alterar!", type='danger'), 400

@app.route("/excluir-usuario/<id>")
def excluirUsuario(id):
    if(db.excluir_usuario(id)):
        result = db.busca_usuarios()
        return render_template("gerenciar-usuarios.html", usuarios=result, msg="Usuário excluído com sucesso!", type='success'), 200
    else:
        result = db.busca_usuarios()
        return render_template("gerenciar-usuarios.html", usuarios=result, msg="Não foi possível excluir", type='danger'), 400

@app.route("/api-consulta-tag/<tag>")
def consultaTag(tag):
    if(db.busca_tag(tag)):
        return jsonify(True)
    else:
        return jsonify(False)

@app.route("/api-consulta-solicitacoes")
def consultaSolicitacoes():
    result = db.busca_solicitacoes()
    try:
        solicitacao = result[0]
        db.efetiva_solicitacao(solicitacao)
        return jsonify(True)
    except:
        return jsonify(False)


@app.route("/api-atualiza-temperatura/<temperatura>")
def atualizaTemperatura(temperatura):
    db.atualiza_temperatura(temperatura)
    return jsonify(True)



#----------------------------------
# MÉTODOS DO SERVER
#----------------------------------

if __name__ == "__main__":
    app.run(debug=True)
