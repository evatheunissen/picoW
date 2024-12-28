from picozero import DistanceSensor
from picozero import Potentiometer
from time import sleep
from machine import Pin

button = Pin(14, Pin.IN, Pin.PULL_DOWN)
led = Pin(15, Pin.OUT)
ds = DistanceSensor(echo=2, trigger = 3, max_distance = 3)
pm = Potentiometer(pin=26)

while True:
    if button.value() == 1:
        for i in range(3):
            led.value(1)
            sleep(0.7)
            led.value(0)
            sleep(0.3)
        
        factor = pm.voltage
        meter_height = 100 + (factor * (200 / 3.3))
        print(f"Current meter height: {meter_height:.2f} cm.")
        
        measured = ds.distance
        if measured != None:
            meter_tohead = measured * 100
            ph_check = meter_height - meter_tohead
            if ph_check > 35:
                if ph_check < 280:
                    patient_height = ph_check
                    print(f"Patient height: {patient_height:.2f} cm.")
  