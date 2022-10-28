from SmartCarModules.servo import *
from SmartCarModules.Ultrasonic import *
import time
import math as m

us = Ultrasonic()
neck = Servo()
ccw = True

def getXY(d, angle_d):
    angle = m.radians(angle_d)
    x = int(d*m.cos(angle))
    y = int(d*m.sin(angle))
    return x, y

while True:
    if ccw:
        start = 30
        end = 155
        change = 5
    else:
        start = 150
        end = 25
        change = -5
            
    for angle in range (start, end, change):
        neck.setServoPwm('0',angle)
        distance = us.get_distance()
        x, y = getXY(distance, angle)
        print(distance, x, y)
        time.sleep(1)
    ccw = not ccw