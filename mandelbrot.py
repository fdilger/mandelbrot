#!/usr/bin/env python3

import pygame
import math
import sys
from threading import Thread
from graphics import color_rgb

pygame.init()
display_width = 800
display_height = 800
screen = pygame.display.set_mode((display_width,display_height))

def mandelbrot_iteration (x0,y0, it):
    x=0
    y=0
    x2=0
    y2=0
    iterations = 0
    while x2+y2 <= 4 and iterations< it:
        y=2*x*y+y0
        x=x2-y2+x0
        x2=x*x
        y2=y*y
        iterations+=1
            
    return iterations,x,y

def palette_lookup(iterations):
    #16777215
    # 16777250
    c=str(hex((int(16777250 -iterations * (16777215/5000) )) % 16777215)).removeprefix("0x")
    # add trailing zeros
    for m in range(6-len(c)):
        c=c+"0"
    return c

def determine_color_cont(x,y,iterations, it):
    tmp= iterations
    if iterations == 2000:
        return "#000000"
    if iterations < 2000:
        log_zn= math.log(x*x+y*y)/2
        nu = math.log(log_zn/math.log(2)) / math.log(2)
        tmp = tmp +1 -nu
    c1 = palette_lookup(math.floor(tmp))
    c2 = palette_lookup(math.floor(tmp)+1)
    rgb1 = tuple(int(c1[i:i+2], 16) for i in (0, 2, 4))
    rgb2 = tuple(int(c2[i:i+2], 16) for i in (0, 2, 4))
    t = tmp % 1
    rgb3 = (math.floor(rgb1[0]+(rgb2[0]-rgb1[0])*t), math.floor(rgb1[1]+(rgb2[1]-rgb1[1])*t) , math.floor(rgb1[2]+(rgb2[2]-rgb1[2])*t)  )
    return color_rgb(rgb3[0],rgb3[1],rgb3[2])
    
def draw_(x,y,offset,zoom):
    for i in range(int(display_width/5)):
        if i%10 == 0:
            pygame.display.update()
        for k in range(display_height):
            iterations = mandelbrot_iteration(x-zoom/2+zoom/display_width*(i+offset),(y-zoom/2+zoom/display_height*k), 2000)
            if iterations[0] > 0: 
                screen.set_at((i+offset,k), determine_color_cont(iterations[1],iterations[2], iterations[0], 2000))
                
    pygame.display.update()
    
def draw_mandelbrot():
    # setup
    exp = -1*int(sys.argv[1])
    zoom = 1.506043553756164*pow(10,exp)
    x = -0.7746806106269039
    y = -0.1374168856037867
    pygame.display.update()
    # create and start threads
    thread1 = Thread(target=draw_, args = (x,y,0,zoom))
    thread2 = Thread(target=draw_, args = (x,y,int(display_width/5),zoom))
    thread3 = Thread(target=draw_, args = (x,y,2*int(display_width/5),zoom))
    thread4 = Thread(target=draw_, args = (x,y,3*int(display_width/5),zoom))
    thread5 = Thread(target=draw_, args = (x,y,4*int(display_width/5),zoom))
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    # prompt for screenshot
    c = input("screenshot? (y/n)")
    if c=="y":
        pygame.image.save(screen, "screenshot.jpeg")

draw_mandelbrot()

        
