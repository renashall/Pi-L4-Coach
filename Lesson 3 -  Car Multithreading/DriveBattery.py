import pygame
from SmartCarModules.Motor import *
from SmartCarModules.Buzzer import *
from SmartCarModules.Led import *
from SmartCarModules.ADC import *
from SmartCarModules.Thread import *
import datetime as dt

width = 1280
height = 720

pygame.init()
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Driving")

font = pygame.font.SysFont("Arial", 48)

buzzer=Buzzer()
led=Led()
adc=Adc()

keep_going = True
keys=pygame.key.get_pressed()
lights = 'off'

battery_percent = 0
battery_color = (255,255,255)

def Battery():
    global battery_percent, battery_color
    while keep_going:
        battery_voltage = adc.recvADC(2) * 3
        battery_percent = int(100*(battery_voltage-6)/(8-6))
        
        if battery_percent > 75:
            battery_color = (0,255,0)
        elif battery_percent > 50:
            battery_color = (255,255,0)
        elif battery_percent > 25:
            battery_color = (255,165,0)
        else:
            battery_color = (255,0,0)
            
        time.sleep(1)
        
def headlight():
    global lights
    while keep_going:
        if adc.recvADC(0) < 0.5 or adc.recvADC(1) < 0.5:
            led.ledIndex('D18',255,255,255)
            led.ledIndex('D17',255,255,255)
            lights = 'on'
        
        elif keys[pygame.K_BACKSPACE] :
            led.turnOffLeds(['D17', 'D18'])
            lights = 'off'
def loop():       
    global keep_going, keys
    direction = 'stopped'
    horn = 'off'
    
    while keep_going:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
        
        screen.fill((0,0,0))
        
        keys=pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            PWM.setMotorModel(800,800,800,800)
            direction = 'forward'
            led.turnOffLeds(['D16', 'D19', 'D13', 'D14'])
        
        elif keys[pygame.K_LEFT]:
            PWM.setMotorModel(-800,-800,1400,1400)
            direction = 'left'
            led.ledIndex('D16',0,255,0)
            led.turnOffLeds(['D19', 'D13', 'D14'])
        
        elif keys[pygame.K_RIGHT]:
            PWM.setMotorModel(1400,1400,-800,-800)
            direction = 'right'
            led.ledIndex('D19',0,255,0)
            led.turnOffLeds(['D16', 'D13', 'D14'])
        
        elif keys[pygame.K_DOWN]:
            PWM.setMotorModel(-600,-600,-600,-600)
            direction = 'reverse'
            led.ledIndex('D13',255,0,0)
            led.ledIndex('D14',255,0,0)
            led.turnOffLeds(['D16', 'D19'])
        else:
            PWM.setMotorModel(0,0,0,0)
            direction = 'stopped'
            led.turnOffLeds(['D16', 'D19', 'D13', 'D14'])
        
        if keys[pygame.K_SPACE]:
            buzzer.run(1)
            horn = 'on'
        else:
            buzzer.run(0)
            horn = 'off'
           
        Drive_Text = font.render("Car: " + direction, True, (255, 255, 255))
        Drive_Text_Rect = Drive_Text.get_rect(center=(width/2, height/6))
        screen.blit(Drive_Text, Drive_Text_Rect)
        
        Buzzer_Text = font.render("Horn: " + str(horn) , True, (255, 255, 255))
        Buzzer_Text_Rect = Buzzer_Text.get_rect(center=(7*width/8, height/6))
        screen.blit(Buzzer_Text, Buzzer_Text_Rect)
        
        Time_Text = font.render("Time: " + dt.datetime.now().strftime("%H:%M"), True, (255,255,255))
        Time_Text_Rect = Time_Text.get_rect(center=(width/8, height/6))
        screen.blit(Time_Text, Time_Text_Rect)
        
        Light_Text = font.render("Lights: " + lights , True, (255, 255, 255))
        Light_Text_Rect = Light_Text.get_rect(center=(width/8, height/3))
        screen.blit(Light_Text, Light_Text_Rect)
        
        Battery_Text = font.render("Battery: " + str(battery_percent) + '%', True, battery_color)
        Battery_Text_Rect = Battery_Text.get_rect(center=(7*width/8, height/3))
        screen.blit(Battery_Text, Battery_Text_Rect)
        
        pygame.display.update()

    pygame.display.quit()
    pygame.quit()

if __name__ == "__main__":
    threads = [threading.Thread(target=headlight),
        threading.Thread(target=Battery)]
    try:
        for t in threads:
            t.start()
        loop()
    except KeyboardInterrupt:
        pygame.display.quit()
        pygame.quit()
        for t in threads:
            stop_thread(t)