# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session, url_for, jsonify
from functools import wraps
import sqlite3, db, datetime


#----------------------------------
# VARIÁVIES GLOBAIS
#----------------------------------
app = Flask(__name__)
tbl_usuarios = 'usuarios'
app.config['SECRET_KEY'] = "A0Zr98j/3yX R~XHH!jmN]/*-+hsHASHsh6 #$$"
_ultimo_minuto = 0
_temperatura_atual = 0
_ultima_leitura = 0

#----------------------------------
# DECORATORS
#----------------------------------
def admin_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if(session and session['usr_nivel'] == '1'):
			return f(*args, **kwargs)
		else:
			return render_template("erros/nao-autorizado.html"), 401
	return wrap

def authorized_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if(db.busca_tag(session['usr_tag'])):
			return test(*args, **kwargs)
		else:
			return render_template("minha-pagina.html", msg="Erro! Você está autorizado?", type='danger'), 401
	return wrap

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session:
            return f(*args, **kwargs)
        else:
            return render_template("erros/nao-logado.html"), 401
    return wrap

#----------------------------------
# ROTAS
#----------------------------------
@app.route("/")
def hello():
    return render_template("index.html", temperatura=_temperatura_atual, datahora=_ultima_leitura), 200

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
@login_required
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
@login_required
def minhaPagina():
    return render_template("minha-pagina.html", temperatura=_temperatura_atual, datahora=_ultima_leitura), 200

@app.route("/pedir-cafe")
@login_required
@authorized_required
def pedirCafe():
	global _temperatura_atual
	global _ultima_leitura
	return render_template("minha-pagina.html", msg="Solicitado!", type='success', temperatura=_temperatura_atual, datahora=_ultima_leitura), 201


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
@admin_required
def gerenciarUsuarios():
    result = db.busca_usuarios()
    return render_template("gerenciar-usuarios.html", usuarios=result), 200

@app.route("/historico")
@admin_required
def historicoFun():
	pedidos = db.busca_historico()
	return render_template('historico.html', pedidos=pedidos)

@app.route("/temperaturas")
@login_required
def temperaturasFun():
	temp = db.busca_temperaturas()
	return render_template('temperaturas.html', temp=temp)

@app.route("/ativar-usuario/<id>")
@admin_required
def ativarUsuario(id):
    if(db.ativar_usuario(id)):
        result = db.busca_usuarios()
        return render_template("gerenciar-usuarios.html",usuarios=result, msg="Alteração feita com sucesso!", type='success'), 200
    else:
        result = db.busca_usuarios()
        return render_template("gerenciar-usuarios.html", msg="Não foi possível alterar!", type='danger'), 400

@app.route("/excluir-usuario/<id>")
@admin_required
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
	global _ultimo_minuto
	_minuto_atual = datetime.datetime.now().strftime("%M")
	if(_minuto_atual != _ultimo_minuto):
		_ultimo_minuto = _minuto_atual
		return jsonify("temperatura")
	else:
	    result = db.busca_solicitacoes()
	    try:
	        solicitacao = result[0]
	        db.efetiva_solicitacao(solicitacao)
	        return jsonify(True)
	    except:
	        return jsonify(False)

@app.route("/api-atualiza-temperatura/<temperatura>")
def atualizaTemperatura(temperatura):
	global _temperatura_atual
	global _ultima_leitura
	_temperatura_atual = temperatura
	_ultima_leitura = datetime.datetime.now().strftime("%H:%M:%S")
	db.atualiza_temperatura(temperatura)
	return jsonify(True)

#----------------------------------
# MÉTODOS DO SERVER
#----------------------------------

if __name__ == "__main__":
    app.run(debug=True)
