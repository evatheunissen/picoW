from picozero import DistanceSensor
from time import sleep
from time import ticks_ms
from machine import Pin

button = Pin(14, Pin.IN, Pin.PULL_DOWN)
led = Pin(15, Pin.OUT)
ds = DistanceSensor(echo=2, trigger = 3, max_distance = 3)
time_start = 0
meter_height = 250

while True:
    if button.value() == 1:
        if time_start == 0:
            time_start = ticks_ms()
    else:
        if time_start != 0:
            start = time_start
            time_start = 0
            if (ticks_ms() - start) >= 3000:
                for i in range(3):
                    led.value(1)
                    sleep(0.3)
                    led.value(0)
                    sleep(0.7)
            
                measured = ds.distance
                if measured != None:
                    if measured < 3:
                        meter_height = measured * 100
                        print(f"Current meter height: {meter_height:.2f} cm.")
            else:
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
                            print(f"Patient height: {patient_height:.2f} cm.")
