#!/usr/bin/env python
#http://picamera.readthedocs.io/en/release-1.10/recipes1.html#overlaying-images-on-the-preview
#http://stackoverflow.com/questions/2659312/how-do-i-convert-a-numpy-array-to-and-display-an-image
#https://www.raspberrypi.org/learning/the-all-seeing-pi/worksheet2/ ==> exactement ce que je veux faire!

import picamera
from PIL import Image
from time import sleep

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 24
    camera.start_preview()

    # Load the arbitrarily sized image
    img = Image.open('overlay.png')
    # Create an image padded to the required size with
    # mode 'RGB'
    pad = Image.new('RGB', (
        ((img.size[0] + 31) // 32) * 32,
        ((img.size[1] + 15) // 16) * 16,
        ))
    # Paste the original image into the padded one
    pad.paste(img, (0, 0))
	
	#test pour sauvegarder l'image pour ne pas repasser par le padding à chaque execution
	#pad.save(
    
	# Add the overlay with the padded image as the source,
    # but the original image's dimensions
    o = camera.add_overlay(pad.tostring(), size=img.size)
    # By default, the overlay is in layer 0, beneath the
    # preview (which defaults to layer 2). Here we make
    # the new overlay semi-transparent, then move it above
    # the preview
    o.alpha = 128
    o.layer = 3

    # Wait indefinitely until the user terminates the script
    while True:
        sleep(1)
