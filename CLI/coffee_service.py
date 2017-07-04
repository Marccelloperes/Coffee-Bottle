import sys
import os
import ujson
import urequests as request
import machine
import time

#-------------------------------------------
# DECLARAÇÃO DAS VARÁVEIS GLOBAIS
#-------------------------------------------
_server_addr = '10.5.16.243'
_server_port = "5000"
_count = 0

#-------------------------------------------
# DECLARAÇÃO DAS VARÁVEIS GLOBAIS DOS PINOS
#-------------------------------------------
_vermelho = None
_amarelo = None
_verde = None
_branco = None
_sensorLuz = None
_buzina = None

#-------------------------------------------
# MÉTODOS
#-------------------------------------------

# Método chamado após a importação deste arquivo no main.py
def start():
    print('Coffee Service iniciado...')

def configuraPinos():
    global _vermelho
    global _verde
    global _amarelo
    global _branco
    global _buzina
    global _sensorLuz
    global _botao

    _vermelho = machine.Pin(15, machine.Pin.OUT)
    _amarelo = machine.Pin(13, machine.Pin.OUT)
    _branco = machine.Pin(14, machine.Pin.OUT)
    _verde = machine.Pin(12, machine.Pin.OUT)
    _buzina = machine.Pin(5, machine.Pin.OUT)
    _botao = machine.Pin(0, machine.Pin.IN)
    _sensorLuz = machine.Pin(2, machine.Pin.IN)

    _vermelho.on()
    _verde.off()
    _amarelo.off()
    _branco.off()
    _buzina.off()

# Método que libera o café
def liberaCafe():
    global _vermelho
    global _verde
    global _amarelo
    global _branco
    global _buzina
    global _sensorLuz
    global _botao

    _vermelho.off()
    time.sleep(2)
    _amarelo.on()
    time.sleep(2)
    _verde.on()
    time.sleep(2)
    _branco.on()
    time.sleep(2)
    print(url)
    try:
        r = request.get(url)
        r.close()
        _vermelho.on()
        _verde.off()
        _amarelo.off()
        _branco.off()
        return True
    except Exception as e:
        print("Coffee Service - liberaCafe(): ", e)
        _vermelho.on()
        _verde.off()
        _amarelo.off()
        _branco.off()
        return False



#Este método é chamado quando uma caneca se aproxima do sensor de proximidade
def consultaSolicitacoes():
    url = "http://" + _server_addr +  ":" +  _server_port +  "/api-consulta-solicitacoes"
    print(url)
    try:
        r = request.get(url)
        response = ujson.loads(r.content)
        r.close()
        if(response):
            liberaCafe()
        return
    except Exception as e:
        print("Coffee Service - consultaSolicitacoes(): ", e)
        return

# Método que verifica se há uma caneca presente
def verificaPinagem():
    global _botao
    if(_botao.value() == 0):
        liberaCafe()
    return

# Método que envia a temperatura para o servidor
def atualizaTemperatura():
    print("Enviando temperatura")
    temp = 70
    url = "http://" + _server_addr +  ":" +  _server_port +  "/api-atualiza-temperatura/" + str(temp)
    print(url)
    try:
        r = request.get(url)
        r.close()
        return
    except Exception as e:
        print("Coffee Service - atualizaTemperatura(): ", e)


configuraPinos()
while 1:
    consultaSolicitacoes()
    verificaPinagem()
    atualizaTemperatura()
    time.sleep(1)





#---------------------------------------------
# MÉTODOS ORIGINAIS
#---------------------------------------------

#Este método é chamado quando uma caneca se aproxima do sensor de proximidade
# def solicitaAutorizacao(tag,):
#     while(_busy):
#         pass
#     _busy = True
#     url = "http://" + _server_addr +  ":" +  _server_port +  "/api-consulta-tag/"  + tag
#     print(url)
#     r = request.get(url)
#     response = ujson.loads(r.content)
#     r.close()
#     if(response == True):
#         print("Yeah!")
#     else:
#         print("Oh, no!")
#     _busy = False


#Este método é chamado quando uma solicitação é feita pelo site
# def liberaCafe(id):
#     while(_busy):
#         time.sleep(1)
#     #url = "http://" + _server_addr +  ":" +  _server_port +  "/api-consulta-tag/"  + tag
#     _busy = True
#     url = "http://" + _server_addr +  ":" +  _server_port +  "/api-registra-pedido/" + id
#     print(url)
#     r = request.get(url)
#     response = ujson.loads(r.content)
#     r.close()
#     if(response == True):
#         print("Yeah!")
#     else:
#         print("Oh, no!")
#     _busy = False
