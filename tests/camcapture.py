#!/usr/bin/env python
#Reaction button controled camera recipe

from gpiozero import Button
from picamera import PiCamera
import time
from signal import pause

white_button = Button(22)
red_button = Button(24)
camera = PiCamera()

def capture():
    datetime = time.strftime("%Y-%m-%d-%H-%M-%S")
    camera.capture('/home/pi/%s.jpg' % datetime)

white_button.when_pressed = camera.start_preview
white_button.when_released = camera.stop_preview
red_button.when_pressed = capture

pause()
