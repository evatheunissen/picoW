from picozero import DistanceSensor
from time import sleep
from time import ticks_ms
from machine import Pin

led = Pin(15, Pin.OUT)
ds = DistanceSensor(echo=2, trigger = 3, max_distance = 3)
        
def calibrate_meterHeight():
    for i in range(3):
        led.value(1)
        sleep(0.3)
        led.value(0)
        sleep(0.7)
            
    measured = ds.distance
    if measured != None:
        if measured < 3:
            meter_height = measured * 100
            return round(meter_height, 2)

def measure_patientHeight(meter_height):    
    for i in range(3):
        led.value(1)
        sleep(0.7)
        led.value(0)
        sleep(0.3)
                
    measured_sec = ds.distance
    if measured_sec != None:
        meter_tohead = measured_sec * 100
        ph_check = meter_height - meter_tohead
        if ph_check > 35:
            if ph_check < 280:
                patient_height = ph_check
                return round(patient_height, 2)
