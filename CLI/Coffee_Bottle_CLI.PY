# -*- coding: latin-1 -*-
from Adafruit_IO import Client, Feed
from threading import Timer
import numpy as np
import time
from wiringx86 import GPIOGalileo as GPIO
from upm import pyupm_jhd1313m1 as lcd

pinoTemp = 16
pinoIR = 3
pinoBotao = 2
pinoRele = 8

tela = lcd.Jhd1313m1(0, 0x3E, 0x62)
tela.clear()
tela.setCursor( 0, 0)
tela.setColor(255, 255, 255)

#Declaração dos GPIOs
botao= GPIO(debug=False)
botao.pinMode(pinoBotao, botao.INPUT)

IR = GPIO(debug=False)
IR.pinMode(pinoIR, IR.INPUT)

rele = GPIO(debug=False)
rele.pinMode(pinoRele, rele.OUTPUT)

temp = GPIO(debug=False)
temp.pinMode(pinoTemp, temp.ANALOG_INPUT)

ADAFRUIT_IO_KEY = 'dfee8fe53e5545398320b5119bd83de3'
ADAFRUIT_IO_USERNAME = 'eraldojr'

aio = Client(ADAFRUIT_IO_KEY)

#Função para liberar o líquido
def liberaLiquido(valor_botao):
    if(valor_botao == 1):
        rele.digitalWrite(pinoRele, rele.HIGH)
    else:
        rele.digitalWrite(pinoRele, rele.LOW)


#Função para exibir a temperatura no LCD
def atualizaTemp(temp_cafe):
    try:
        print (temp_cafe)
        tela.clear()
        tela.setCursor( 0, 0)
        tela.write("Temp. do cafe:")
        tela.setCursor( 1, 0)
        tela.write(format(temp_cafe))
    except KeyboardInterrupt:
        print '\nDesligando o Lcd'
        tela.clear()
        tela.displayOff()
        tela.backlightOff()

def main():
    print("Iniciado")
    while(1):
        temperatura = temp.analogRead(pinoTemp)
        valor_botao = botao.digitalRead(pinoBotao)
        atualizaTemp(temperatura)
        liberaLiquido(valor_botao)
        time.sleep(1)
main()
