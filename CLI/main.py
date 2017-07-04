import os
import sys
import network
import time

#Método que exibe o menu para se conectar a WLAN
def conectaWLAN():
    import os
    import sys
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        print("Rede já conectada com as configurações: ", wlan.ifconfig())
        print("Deseja fazer nova conexão? [Y/N]")
        opt = sys.stdin.readline()
        opt = opt.rstrip('\n')
        if opt == 'Y' or opt == 'y':
            tentaConectar(wlan)
        else:
            print("Configurações de rede mantidas:", wlan.ifconfig())
    else:
        i=0
        while(i != 1 and wlan.isconnected() == False):
            print("Rede não conectada. Deseja verificar novamente? [Y/N]")
            opt = sys.stdin.readline()
            opt = opt.rstrip('\n')
            if opt != 'Y' and opt != 'y':
                i = 1
        tentaConectar(wlan)

#Método que se conecta a WLAN
def tentaConectar(wlan):
    print("Por favor, informe o SSID da rede WLAN:")
    essid = sys.stdin.readline()
    essid = essid.rstrip('\n')
    print("SSID: ", essid)
    print("Agora informe a senha:")
    pwd = sys.stdin.readline()
    pwd = pwd.rstrip('\n')
    print("Senha: ",pwd)
    print("Conectando...")
    wlan.connect(essid, pwd)
    while not wlan.isconnected():
        pass
    print("Configurações da rede:", wlan.ifconfig())



conectaWLAN()
import coffee_service as cs
