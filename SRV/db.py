# -*- coding: utf-8 -*-
from flask import session
import datetime
import sqlite3
import scipy
import db

# Método para efetuar login
def valida_login(_email, _senha):
    try:
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(''' SELECT * FROM usuarios WHERE email = ? AND senha = ?''', (_email, _senha))
        connect.commit()
        result = scipy.array(cursor.fetchall())
        usuario = result[0]
        if usuario.size:
            return usuario
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
        cursor.execute('''INSERT INTO usuarios (nome, email, senha, nivel, ativo) VALUES (?,?,?,?,?)''', (_nome, _email, _senha, 2, 0))
        connect.commit()
        connect.close()
        return True
    except Exception as e:
        print ('novo_usuario(): ', e)
        return False

# Método para buscar todos usuários, exceto admin (Nivel 1)
def busca_usuarios():
    try:
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(''' SELECT * FROM usuarios WHERE nivel != 1''')
        connect.commit()
        result = scipy.array(cursor.fetchall())
        return result
    except Exception as e:
        print ('busca_usuarios(): ', e)
        return False

# Método para excluir usuário
def excluir_usuario(_id):
    try:
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('''DELETE FROM usuarios WHERE id = ?''', (_id))
        connect.commit()
        connect.close()
        return True
    except Exception as e:
        print ('excluir_usuario(): ', e)
        return False

# Método para ativar/desativar usuário. Se estiver ativo, desativa. Caso contrário, ativa.
def ativar_usuario(_id):
    try:
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('''SELECT ativo FROM usuarios WHERE id = ?''', (_id))
        connect.commit()
        result = scipy.array(cursor.fetchall())
        result_ativo = result[0]
        if result_ativo == 1:
            result_ativo = 0
        else:
            result_ativo = 1
        cursor.execute('''UPDATE usuarios SET ativo = ?  WHERE id = ?''', (result_ativo, _id))
        connect.commit()
        connect.close()
        return True
    except Exception as e:
        print ('ativar_usuario(): ', e)
        return False

# Método que busca a tag e verifica que o usuário está ativo
# Se estiver tudo OK, registra a solicitação no histórico
def busca_tag(tag):
        try:
            tag = tag + ""
            connect = sqlite3.connect('database.db')
            cursor = connect.cursor()
            cursor.execute('SELECT id, ativo FROM usuarios WHERE tag = ?', (tag,))
            connect.commit()
            result = scipy.array(cursor.fetchall())
            ativo = 0
            _id = result[0][0]
            ativo = result[0][1]
            if ativo == 1:
                try:
                    data_hora = datetime.datetime.now().strftime("%Y%m%d-%H:%M")
                    connect = sqlite3.connect('database.db')
                    cursor = connect.cursor()
                    cursor.execute('''INSERT INTO historico (id_usuario, data_hora, status) VALUES (?,?, 0)''', (int(_id), data_hora,))
                    connect.commit()
                    connect.close()
                    return True
                except Exception as err:
                    print ('busca_tag() -> Ao inserir no historico: ', err)
                    return False
        except Exception as e:
            print ('busca_tag(): ', e)
            return False

# Método que busca as solicitacoes do historico com status 0
# Solicitacoes com status 0 estão aguardando e 1 estão concluídas
def busca_solicitacoes():
        try:
            connect = sqlite3.connect('database.db')
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM historico WHERE status = 0')
            connect.commit()
            result = scipy.array(cursor.fetchall())
            if(result.size):
                return result
            else:
                return False
        except Exception as e:
            print ('busca_solicitacoes(): ', e)
            return False

# Atualiza o status da solicitacao que foi aceita para 1, ou seja, concluída
def efetiva_solicitacao(solicitacao):
    try:
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        _id = solicitacao[0]
        cursor.execute('''UPDATE historico SET status = 1 WHERE  id = ? ''', (int(_id),))
        connect.commit()
        connect.close()
        return True
    except Exception as e:
        print ('efetiva_solicitacao(): ', e)
        return False

# Insere uma nova temperatura no banco
def atualiza_temperatura(temp):
    try:
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        data_hora = datetime.datetime.now().strftime("%Y%m%d-%H:%M")
        cursor.execute('''INSERT INTO temperatura (valor, data_hora) VALUES (?,?) ''', (temp, data_hora,))
        connect.commit()
        connect.close()
        return True
    except Exception as e:
        print ('atualiza_temperatura(): ', e)
        return False
