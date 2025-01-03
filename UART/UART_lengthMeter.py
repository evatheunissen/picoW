from machine import Pin, UART
from time import sleep
from functions_lengthMeter import calibrate_meterHeight, measure_patientHeight

uart = UART(0, baudrate = 9600, tx = Pin(0), rx = Pin(1))
uart.init(bits = 8, parity = None, stop = 2)

led = Pin(15, Pin.OUT)

buffer = ""

mh = 250
ph = None

def uart_callback(data):
    global buffer, mh, ph
    data = uart.read()
    if data == b'\r':
        #print(f"{buffer}")
        if buffer == "calibrate":
            mh = calibrate_meterHeight()
            uart.write("Meter height: " + str(mh) + " cm.\r\n")
        elif buffer == "measure":
            ph = measure_patientHeight(mh)
            uart.write("Patient height: " + str(ph) + " cm.\r\n")
        buffer = ""
    else:
        buffer += data.decode('utf-8')
        

uart.irq(handler = uart_callback, trigger = UART.IRQ_RXIDLE, hard = False)
