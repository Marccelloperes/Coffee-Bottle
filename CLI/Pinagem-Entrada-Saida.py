import machine

D8 - gpio15 = machine.Pin(15, machine.Pin.IN) -> Escrita
D7 - gpio13 = machine.Pin(13, machine.Pin.IN) -> Escrita
D6 - gpio12 = machine.Pin(12, machine.Pin.IN) -> Escrita
D5 - gpio14 = machine.Pin(14, machine.Pin.IN) -> Escrita
D4 - gpio2 = machine.Pin(2, machine.Pin.IN) ->  Escrita / Leitura
D3 - gpio0 = machine.Pin(0, machine.Pin.IN) -> Escrita / Leitura
D2 - gpio4 = machine.Pin(4, machine.Pin.IN) -> Escrita
D1 - gpio5 = machine.Pin(5, machine.Pin.IN) -> Escrita




botao.irq(trigger=botao.IRQ_RISING, handler=mostra)

busy = False
def mostra(pin):
    while(busy):
        time.sleep(1)
busy = True
print("Pino alterado", pin)
time.sleep(1)
busy = False
