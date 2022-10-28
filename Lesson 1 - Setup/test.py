import time
from SmartCarModules.Led import *
from SmartCarModules.Motor import *
from SmartCarModules.Ultrasonic import *
from SmartCarModules.Line_Tracking import *
from SmartCarModules.servo import *
from SmartCarModules.ADC import *
from SmartCarModules.Buzzer import *

def test_Led():
    print("LED Test")
    try:
        led.ledIndex(0,255,0,0)      #Red
        led.ledIndex(1,255,125,0)    #orange
        led.ledIndex(2,255,255,0)    #yellow
        led.ledIndex(3,0,255,0)      #green
        led.ledIndex(4,0,255,255)    #cyan-blue
        led.ledIndex(5,0,0,255)      #blue
        led.ledIndex(6,128,0,128)    #purple
        led.ledIndex(7,255,255,255)  #white'''
        print ("The LED has been lit, the color is red orange yellow green cyan-blue blue white")
        time.sleep(3)               #wait 3s
    finally:
        led.colorWipe(led.strip, Color(0,0,0))  #turn off the light
        print ("\nEnd of program")
        
def test_Motor():
    print("Motor Test")
    try:
        PWM.setMotorModel(1000,1000,1000,1000)       #Forward
        print ("The car is moving forward")
        time.sleep(1)
        PWM.setMotorModel(-1000,-1000,-1000,-1000)   #Back
        print ("The car is going backwards")
        time.sleep(1)
        PWM.setMotorModel(-1500,-1500,2000,2000)       #Left 
        print ("The car is turning left")
        time.sleep(1)
        PWM.setMotorModel(2000,2000,-1500,-1500)       #Right 
        print ("The car is turning right")  
        time.sleep(1)
    finally:
        PWM.setMotorModel(0,0,0,0)
        print ("\nEnd of program")
               
def test_Ultrasonic():
    print("Ultrasonic Test")
    try:
        for i in range(3):
            data=ultrasonic.get_distance()   #Get the value
            print ("Obstacle distance is "+str(data)+"CM")
            time.sleep(1)
    finally:
        print ("\nEnd of program")

def test_Infrared():
    print("IR Line Sensor Test")
    try:
        for i in range(5):
            if GPIO.input(line.IR01)!=True and GPIO.input(line.IR02)==True and GPIO.input(line.IR03)!=True:
                print ('Middle')
            elif GPIO.input(line.IR01)!=True and GPIO.input(line.IR02)!=True and GPIO.input(line.IR03)==True:
                print ('Right')
            elif GPIO.input(line.IR01)==True and GPIO.input(line.IR02)!=True and GPIO.input(line.IR03)!=True:
                print ('Left')
            else:
                print("None")
            time.sleep(1)
    finally:
        print ("\nEnd of program")

def test_Servo():
    print("Servo Test")
    try:
        for i in range(50,110,1):
            pwm.setServoPwm('0',i)
            time.sleep(0.01)
        for i in range(110,50,-1):
            pwm.setServoPwm('0',i)
            time.sleep(0.01)
        for i in range(80,150,1):
            pwm.setServoPwm('1',i)
            time.sleep(0.01)
        for i in range(150,80,-1):
            pwm.setServoPwm('1',i)
            time.sleep(0.01)   
    finally:
        pwm.setServoPwm('0',90)
        pwm.setServoPwm('1',90)
        print ("\nEnd of program")

def test_Adc():
    print("ADC Test")
    try:
        Left_IDR=adc.recvADC(0)
        print ("The photoresistor voltage on the left is "+str(Left_IDR)+"V")
        Right_IDR=adc.recvADC(1)
        print ("The photoresistor voltage on the right is "+str(Right_IDR)+"V")
        Power=adc.recvADC(2)
        print ("The battery voltage is "+str(Power*3)+"V")
        time.sleep(1)
        print ('\n')
    finally:
        print ("End of program")

def test_Buzzer():
    print("Buzzer Test")
    try:
        buzzer.run(1)
        time.sleep(1)
    finally:
        buzzer.run(0)
        print ("\nEnd of program")
           
# Main program logic follows:
if __name__ == '__main__':
    print ('Car Test')

    led=Led()
    PWM=Motor()
    ultrasonic=Ultrasonic()
    line=Line_Tracking()
    pwm=Servo()
    adc=Adc()
    buzzer=Buzzer()
    
    test_Led()
    test_Motor()
    test_Ultrasonic()
    test_Infrared()        
    test_Servo()               
    test_Adc()  
    test_Buzzer()
    
    print("Test complete.")

        
        
        
        
