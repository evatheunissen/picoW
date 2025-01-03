from machine import Pin, UART
from time import sleep

uart = UART(0, baudrate = 9600, tx = Pin(0), rx = Pin(1))
uart.init(bits = 8, parity = None, stop = 2)

button = Pin(14, Pin.IN, Pin.PULL_DOWN)
led = Pin(15, Pin.OUT)

uart.write('\r\n')

while True:
    if button.value() == 1:
        uart.write('hello world\r\n')
        sleep(1)
    if uart.any():
        data = uart.read()
        #print(f"{data}")
        if data == b'l':
            led.toggle()
            uart.write('\r\n')
