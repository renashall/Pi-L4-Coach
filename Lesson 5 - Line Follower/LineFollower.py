import time
from SmartCarModules.Motor import *
import RPi.GPIO as GPIO

class Line_Tracking:
    def __init__(self):
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
    
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01,GPIO.IN)
        GPIO.setup(self.IR02,GPIO.IN)
        GPIO.setup(self.IR03,GPIO.IN)
        
    def run(self):
        while True:
            L = GPIO.input(self.IR01)
            M = GPIO.input(self.IR02)
            R = GPIO.input(self.IR03)
            
            self.LMR= L*4 + M*2 + R
            
            if self.LMR == 0b001: #Right activated, left turn
                PWM.setMotorModel(2500,2500,-1500,-1500)
            
            elif self.LMR == 0b010: #Middle activated, go forward
                PWM.setMotorModel(800,800,800,800)
            
            elif self.LMR == 0b011: #Middle and right activated, left turn
                PWM.setMotorModel(4000,4000,-2000,-2000)
            
            elif self.LMR == 0b100: #left, right turn
                PWM.setMotorModel(-1500,-1500,2500,2500)
            
            elif self.LMR == 0b101: #The sides are activated
                #Could be used as a special condition
                PWM.setMotorModel(0,0,0,0)
            
            elif self.LMR == 0b110: #left and middle, right turn
                PWM.setMotorModel(-2000,-2000,4000,4000)
            
            elif self.LMR == 0b111: #All activated, stop line
                PWM.setMotorModel(0,0,0,0)
                
            elif self.LMR == 0b000: #None Activated: Car fell off the track
                t0 = time.time()
                while not(GPIO.input(self.IR01)|GPIO.input(self.IR02)|GPIO.input(self.IR03)):
                    if ((time.time() - t0) > 0.5):
                        PWM.setMotorModel(0,0,0,0)
            
infrared=Line_Tracking()

if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:
        PWM.setMotorModel(0,0,0,0)

