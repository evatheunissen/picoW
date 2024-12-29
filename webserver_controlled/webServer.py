import network
import socket
from time import sleep
from machine import Pin
import machine
import rp2
import sys
from lengthMeter_webControlled import calibrate_meterHeight, measure_patientHeight

led = Pin(15, Pin.OUT)

# Stel volgende parameters in volgens het aanwezige netwerk:
ssid = ''
password = ''

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        if rp2.bootsel_button() == 1:
            sys.exit()
        print('Waiting for connection...')
        led.value(1)
        sleep(0.5)
        led.value(0)
        sleep(0.5)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
    
def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(mh, ph):
    html = f"""
            <!DOCTYPE html>
            <html>
                <body style="max-width: max-content; margin: auto; text-align: center; font-family: Verdana">
                    <h1 style="padding-top: 50px">BeWell Kiosk</h1>
                    <h3 style="padding-bottom: 50px">Lengtemeting</h3>
                    <form action="./calibrate" style="display: inline-block">
                        <input type="submit" value="Calibrate" style="font-size: 16px; margin: 4px 2px; cursor: pointer; background-color: #04AA6D; border: none; color: white; padding: 15px 32px"/>
                    </form>
                    <form action="./measure" style="display: inline-block">
                        <input type="submit" value="Measure" style="font-size: 16px; margin: 4px 2px; cursor: pointer; background-color: #04AA6D; border: none; color: white; padding: 15px 32px"/>
                    </form>
                    <form action="./close" style="display: inline-block">
                        <input type="submit" value="Stop server" style="font-size: 16px; margin: 4px 2px; cursor: pointer; background-color: #ff1447; border: none; color: white; padding: 15px 32px"/>
                    </form>
                    <div style="display: flex; padding-top: 150px; padding-bottom: 50px">
                        <div style="flex: 1">
                            <p style="font-size: 16px">Meter height:</p>
                            <p style="font-size: 28px; color: #04AA6D">{mh} cm</p>
                        </div>
                        <div style="flex: 1">
                            <p style="font-size: 16px">Patient height:</p>
                            <p style="font-size: 28px; color: #04AA6D">{ph} cm</p>
                        </div>
                    </div>
                </body>
            </html>
            """
    return str(html)
    
def serve(connection):
    mh = 250
    ph = None
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/calibrate?':
            mh = calibrate_meterHeight()
            ph = None
        elif request == '/measure?':
            if mh != None:
                ph = measure_patientHeight(mh)
        elif request == '/close?':
            connection.close()
            sys.exit()
        html = webpage(mh, ph)
        client.send(html)
        client.close()
 
ip = connect()
connection = open_socket(ip)    
serve(connection)
