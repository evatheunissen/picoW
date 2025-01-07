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
            # convert from m to cm:
            meter_height = measured * 100
            return round(meter_height, 2)


def measure_patientHeight(meter_height, measure_times, max_deviation):
    for i in range(3):
        led.value(1)
        sleep(0.7)
        led.value(0)
        sleep(0.3)
                
    measured_add = 0
    fault = 0
    
    for i in range(measure_times):
        d = ds.distance
        print(f"{i}. Distance: {d} (in m)")
        if d != None:
            if i != 0:
                if abs(d - (measured_add / i)) < max_deviation:
                    measured_add += d
                    if i != measure_times - 1:
                        sleep(0.2)
                else:
                    fault = 1
                    break;
            else:
                measured_add += d
                sleep(0.2)
        else:
            fault = 1
            break;
    
    #print(f"\r")
    
    if fault == 0:
        measured_result = measured_add / measure_times
        # convert from m to cm:
        meter_tohead = measured_result * 100
        ph_check = meter_height - meter_tohead
        if ph_check > 35: # (meter_height always < 300 cm) !!! if meter_tohead measures max distance of sensor ór higher, it will take the value of 300 cm -> unreliable, but ph_check will be < 0 (and < 35) in that case and the unreliable value will not be used  
            if ph_check < 280:
                patient_height = ph_check
                return round(patient_height, 2)
