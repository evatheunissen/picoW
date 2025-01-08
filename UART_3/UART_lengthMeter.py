from machine import Pin, UART
from time import sleep
from functions_lengthMeter_v2 import calibrate_meterHeight, measure_patientHeight

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
        print(f"\r")
        #print(f"{buffer}\r")
        if buffer == "calibrate":
            mh = calibrate_meterHeight()
            uart.write("Meter height: " + str(mh) + " cm.\r\n")
        elif buffer == "measure":
            ph = measure_patientHeight(mh, 1, 0.0)
            uart.write("Patient height: " + str(ph) + " cm.\r\n")
        elif "measures" in buffer:
            contains = 0
            not_provided = 0
            err = 0
            shots = 0
            dev = 0
            arr = buffer.split()
            for i in range(len(arr)):
                #print(f"{arr[i]}\r")
                if arr[i] == "measures":
                    contains = 1
                    break
            if contains == 1:
                if len(arr) > 1:
                    if len(arr) < 4:
                        try:
                            shots = int(arr[0])
                        except ValueError:
                            print(f"The advanced measure command did not contain a shots value (integer).\r")
                            not_provided += 1
                            shots = 5
                            if len(arr) != 2:
                                err = 1
                        try:
                            dev = float(arr[len(arr) - 1]) / 100 # convert to m, user input is in cm
                        except ValueError:
                            print(f"The advanced measure command did not contain a maximum deviation value (float).\r")
                            not_provided += 1
                            dev = 0.05
                            if len(arr) != 2:
                                err = 1
                        if err == 0:
                            if not_provided < 2:
                                print(f"Shots: {shots}, dev: {dev}.\r")
                                ph = measure_patientHeight(mh, shots, dev)
                                uart.write("Patient height: " + str(ph) + " cm.\r\n")
                else:
                    print(f"Standard advanced measure command.\r")
                    ph = measure_patientHeight(mh, 5, 0.05)
                    uart.write("Patient height: " + str(ph) + " cm.\r\n")
        buffer = ""
    elif data == b'\x7f': # backspace (Michiel)
        buffer = buffer[:-1]
    else:
        buffer += data.decode('utf-8')
        

uart.irq(handler = uart_callback, trigger = UART.IRQ_RXIDLE, hard = False)
