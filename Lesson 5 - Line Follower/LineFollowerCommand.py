import time
from SmartCarModules.Motor import *
from SmartCarModules.Buzzer import *
from SmartCarModules.Thread import *
from SmartCarModules.Ultrasonic import *
from SmartCarModules.Thread import *

import RPi.GPIO as GPIO

class Line_Tracking:
    def __init__(self):
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        
        self.us = Ultrasonic()
        self.buzzer = Buzzer()
        self.safe = True
        self.command = [0,0,0,0]
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01,GPIO.IN)
        GPIO.setup(self.IR02,GPIO.IN)
        GPIO.setup(self.IR03,GPIO.IN)
        
    def move(self):
        L = GPIO.input(self.IR01)
        M = GPIO.input(self.IR02)
        R = GPIO.input(self.IR03)
        
        self.LMR= L*4 + M*2 + R
        
        PWM.setMotorModel(self.command[0], self.command[1], self.command[2], self.command[3])
 
        if self.LMR == 0b001: #Right activated, left turn
            self.command = [2500,2500,-1500,-1500]
            
        elif self.LMR == 0b010: #Middle activated, go forward
            self.command = [800,800,800,800]
        
        elif self.LMR == 0b011: #Middle and right activated, left turn
            self.command = [4000,4000,-2000,-2000]
        
        elif self.LMR == 0b100: #left, right turn
            self.command = [-1500,-1500,2500,2500]
        
        elif self.LMR == 0b101: #The sides are activated
            #Could be used as a special condition
            self.command = [0,0,0,0]
        
        elif self.LMR == 0b110: #left and middle, right turn
            self.command = [-2000,-2000,4000,4000]
        
        elif self.LMR == 0b111: #All activated, stop line
            self.command = [0,0,0,0]
            
        elif self.LMR == 0b000: #None Activated: Car fell off the track
            t0 = time.time()
            while not(GPIO.input(self.IR01)|GPIO.input(self.IR02)|GPIO.input(self.IR03)):
                if ((time.time() - t0) > 1):
                    self.command = [0,0,0,0]
        
    def distanceSafe(self):
        unsafe = 20
        reads = 5
        threshold = 3
        sleepTime = .0005
        
        while True:
            hits = 0
            for i in range(reads):
                if (self.us.get_distance() < unsafe):
                    hits += 1
                time.sleep(sleepTime)
            
            if hits > threshold:
                self.safe = False
            else:
                self.safe = True
    
    def run(self):
        while True:
            if (self.safe):
                self.move()
            else:
                PWM.setMotorModel(0,0,0,0)
                self.buzzer.run(1)
                time.sleep(0.5)
                self.buzzer.run(0)
                time.sleep(2)

if __name__ == '__main__':
    print ('Program is starting ... ')
    infrared=Line_Tracking()
    sonarThread = threading.Thread(target=infrared.distanceSafe)
    
    try:
        sonarThread.start()
        infrared.run()
    except KeyboardInterrupt:
        stop_thread(sonarThread)
        PWM.setMotorModel(0,0,0,0)