#!/usr/bin/env python
#Reaction game recipe

from gpiozero import Button, LED
from time import sleep
import random

led1 = LED(27)
led2 = LED(23)

player_1 = Button(22)
player_2 = Button(24)

led2.blink(on_time=1, off_time=1, n=10, background=True)

time = random.uniform(5, 10)
sleep(time)
led1.on()


while True:
    if player_1.is_pressed:
        print("Player 1 wins!")
        break
    if player_2.is_pressed:
        print("Player 2 wins!")
        break
    
    

led1.off()
