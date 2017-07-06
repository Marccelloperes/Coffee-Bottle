import sys, os, ujson, time, machine
import urequests as request
from machine import ADC

#-------------------------------------------
# DECLARAÇÃO DAS VARÁVEIS GLOBAIS
#-------------------------------------------
_server_addr = '192.168.25.3'
_server_port = "5000"
_count = 0

#-------------------------------------------
# DECLARAÇÃO DAS VARÁVEIS GLOBAIS DOS PINOS
#-------------------------------------------
_vermelho = None
_amarelo = None
_verde = None
_verde_temp = None
_branco = None
_sensorLuz = None
_sensorTemp = None

#-------------------------------------------
# MÉTODOS
#-------------------------------------------

# Método chamado após a importação deste arquivo no main.py
def start():
    print('Coffee Service iniciado...')

def configuraPinos():
    global _vermelho
    global _verde
    global _verde_temp
    global _amarelo
    global _branco
    global _sensorLuz
    global _botao
    global _sensorTemp

    _vermelho = machine.Pin(15, machine.Pin.OUT)
    _amarelo = machine.Pin(13, machine.Pin.OUT)
    _branco = machine.Pin(14, machine.Pin.OUT)
    _verde = machine.Pin(12, machine.Pin.OUT)
    _verde_temp = machine.Pin(5, machine.Pin.OUT)
    _botao = machine.Pin(0, machine.Pin.IN)
    _sensorLuz = machine.Pin(2, machine.Pin.IN)
    _sensorTemp = ADC(0)

    _branco.on()
    _vermelho.off()
    _verde.off()
    _verde_temp.off()
    _amarelo.off()

# Método que libera o café
def liberaCafe():
    global _verde
    global _amarelo
    global _branco

    _branco.off()
    _vermelho.on()
    time.sleep(2)
    _amarelo.on()
    time.sleep(2)
    _verde.on()
    time.sleep(2)

    _vermelho.off()
    _verde.off()
    _amarelo.off()
    _branco.on()
    return True

#Este método é chamado quando uma caneca se aproxima do sensor de proximidade
def consultaSolicitacoes():
    url = "http://" + _server_addr +  ":" +  _server_port +  "/api-consulta-solicitacoes"
    print(url)
    try:
        r = request.get(url)
        response = ujson.loads(r.content)
        r.close()
        if(response == "temperatura"):
            atualizaTemperatura()
        elif response:
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
    global _verde_temp
    global _branco
    global _sensor_temp
    _branco.off()
    _verde_temp.on()
    print("Enviando temperatura")
    temp = _sensorTemp.read()
    temp /=3
    url = "http://" + _server_addr +  ":" +  _server_port +  "/api-atualiza-temperatura/" + str(temp)
    print(url)
    try:
        r = request.get(url)
        r.close()
        _verde_temp.off()
        _branco.on()
        return True
    except Exception as e:
        print("Coffee Service - atualizaTemperatura(): ", e)
        return False


configuraPinos()
while 1:
    consultaSolicitacoes()
    verificaPinagem()
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
