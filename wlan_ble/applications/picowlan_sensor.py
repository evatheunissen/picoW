from picowlan import wlan, load_index
from picozero import pico_temp_sensor, pico_led
from functions_lengthMeter_v2 import calibrate_meterHeight, measure_patientHeight
import sys

html = load_index("index.html")

'''
pico_led.on()
state = 'ON'
temperature = 0
'''

mh = 250
ph = None

def http_handler(request):
    '''
    global state, temperature
    if request == '/lighton?':
        pico_led.on()
        state = 'ON'
    elif request =='/lightoff?':
        pico_led.off()
        state = 'OFF'
    elif request == '/close?':
        sys.exit()
    temperature = pico_temp_sensor.temp
    html2 = html.replace("{state}", state)
    html2 = html2.replace("{temperature}", str(temperature))
    '''
    global mh, ph
    if request == '/calibrate?':
        mh = calibrate_meterHeight()
        ph = None
    elif request == '/measure?':
        ph = measure_patientHeight(mh, 1, 0.0)
        print(f"\r")
    elif request == '/advanced_measure?':
        ph = measure_patientHeight(mh, 5, 0.05)
        print(f"\r")
    elif request == '/close?':
        sys.exit()
    html2 = html.replace("{mh}", str(mh))
    html2 = html2.replace("{ph}", str(ph))
    return str(html2)

wlan("wlan.txt", http_handler)