import pygame
from SmartCarModules.servo import *
from SmartCarModules.Ultrasonic import *
import math as m
import time

width = 1280
height = 720

pygame.init()
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Sonar")

font = pygame.font.SysFont("Arial", 48)

us = Ultrasonic()
neck = Servo()

def getXY(d, angle_d):
    angle = m.radians(angle_d)
    x = int(d*m.cos(angle))
    y = int(d*m.sin(angle))
    return x, y

def loop():
    keep_going = True
    ccw = True
    
    while keep_going:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
        
        screen.fill((0,0,0))

        if ccw:
            start = 30
            end = 155
            change = 5
        else:
            start = 150
            end = 25
            change = -5
            
        for angle in range (start, end, change):
            neck.setServoPwm('0', angle)
            distance = us.get_distance()
            x,y = getXY(distance, angle)
            
            posx = x*10 + width/2
            posy = height-y*10
            
            object_rect = pygame.Rect((posx, posy), (25, 25))
            pygame.draw.rect(screen, (255,0,0), object_rect)
                        
            time.sleep(1)
        ccw = not ccw
        
        pygame.display.update()
    pygame.display.quit()
    pygame.quit()

if __name__ == "__main__":
    
    try:
        loop()
    except KeyboardInterrupt:
        pygame.display.quit()
        pygame.quit()