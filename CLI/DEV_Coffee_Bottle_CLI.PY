# -*- coding: latin-1 -*-
from Adafruit_IO import Client, Feed
from threading import Timer
import numpy as np
import time
from sys import stdin as _in

pinoTemp = 16
pinoIR = 3
pinoBotao = 2
pinoRele = 8

ADAFRUIT_IO_KEY = 'dfee8fe53e5545398320b5119bd83de3'
ADAFRUIT_IO_USERNAME = 'eraldojr'

aio = Client(ADAFRUIT_IO_KEY)

#Função para liberar o líquido
def liberaLiquido(valor_botao):
    if(valor_botao == 1):
        print ("Rele ligado")
    else:
        print ("Rele desligado")


def main():
    print("Iniciado")
    while(1):
        x = _in.readline()
        x = int(x)
        liberaLiquido(x)
        time.sleep(1)
main()
