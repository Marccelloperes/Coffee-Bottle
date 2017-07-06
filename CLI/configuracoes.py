import webrepl_setup



#Método para se conectar a WLAN
def conectaWLAN():
    import os
    import sys
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando a rede...")
        wlan.connect('QUERO CAFE', 'cafe2017')
        while not wlan.isconnected():
            pass
    print("Configurações da rede:", wlan.ifconfig())
conectaWLAN()


#Executar esses códigos para gravar o main.py
import os
m = open('main.py','w')
m.write('''def conectaWLAN():\n    import os\n    import sys\n    import network\n    wlan = network.WLAN(network.STA_IF)\n    wlan.active(True)\n    if not wlan.isconnected():\n        print("Conectando a rede...")\n        wlan.connect('QUERO CAFE', 'cafe2017')\n        while not wlan.isconnected():\n            pass\n    print("Configurações da rede:", wlan.ifconfig())\nconectaWLAN()''')

#Após conectar à WLAN configrar o WebREPL
import webrepl_setup

webrepl.start()
