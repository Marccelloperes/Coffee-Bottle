# -*- coding: utf-8 -*-
from flask import session
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
        for usuario in result:
            print(usuario)
            if(usuario[2] == ''):
                return False;
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
