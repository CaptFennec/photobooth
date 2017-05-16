#!/usr/bin/env python
# created by chris@drumminhands.com
# see instructions at http://www.drumminhands.com/2014/06/15/raspberry-pi-photo-booth/

import os
import glob
import time
import traceback
from time import sleep
#import RPi.GPIO as GPIO
from gpiozero import LED, Button
import picamera # http://picamera.readthedocs.org/en/release-1.4/install2.html
import atexit
import sys
import socket
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
#import pytumblr # https://github.com/tumblr/pytumblr
import config # this is the config python file config.py
from signal import alarm, signal, SIGALRM, SIGKILL

########################
### Variables Config ###
########################

yled = LED(27, active_high=True, initial_value=False) # pin definition for yellow button LED, active high (GPIO-resistor-long_LED_short-GND), off by default
rled = LED(23, active_high=True, initial_value=False) # pin definition for red button LED, active high (GPIO-resistor-long_LED_short-GND), off by default

ybutton = Button(22, pull_up=True, bounce_time=0.3, hold_time=3, hold_repeat=False) # pin definition for yellow button
rbutton = Button(24, pull_up=True, bounce_time=0.3, hold_time=3, hold_repeat=False) # pin definition for red button

# full frame of v1 camera is 2592x1944. Wide screen max is 2592,1555
# if you run into resource issues, try smaller, like 1920x1152. 
# or increase memory http://picamera.readthedocs.io/en/release-1.12/fov.html#hardware-limits
high_res_w = 2592 # width of high res image, if taken
high_res_h = 1944 # height of high res image, if taken

#############################
### Variables that Change ###
#############################
# Do not change these variables, as the code will change it anyway
total_pics = 1 # number of pics to be taken
transform_x = config.monitor_w # how wide to scale the image when replaying
transfrom_y = config.monitor_h # how high to scale the image when replaying
offset_x = 0 # how far off to left corner to display photos
offset_y = 0 # how far off to left corner to display photos


####################
### Other Config ###
####################
real_path = os.path.dirname(os.path.realpath(__file__)) # path to script

# GPIO setup # desactivated for gpio zero use instead
#GPIO.output(led_pin,False) #for some reason the pin turns on at the beginning of the program. Why?

# initialize pygame
pygame.init()
pygame.display.set_mode((config.monitor_w, config.monitor_h))
screen = pygame.display.get_surface()
pygame.display.set_caption('Photo Booth Pics') # set from config file, was 'Photo Booth Pics'
pygame.mouse.set_visible(False) #hide the mouse cursor
pygame.display.toggle_fullscreen()

#################
### Functions ###
#################

# clean up running programs as needed when main program exits
def cleanup():
  print('Ended abruptly') 
  pygame.quit()
#  GPIO.cleanup() # was used by RPi.GPIO. Needed for gpiozero?
atexit.register(cleanup) # ça fait quoi?

# A function to handle keyboard/mouse/device input events    
def input(events):
    for event in events:  # Hit the ESC key to quit the slideshow.
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)): # escape or ctrl-c detection?
            pygame.quit()
                
#delete files in folder
def clear_pics(channel):
	files = glob.glob(config.file_path + '*')
	for f in files:
		os.remove(f) 
	#light the lights in series to show completed
	print('Deleted previous pics') 
	
	yled.blink(on_time=1, off_time=1, n=3, background=True)
	rled.blink(on_time=1, off_time=1, n=3, background=False) # simultaneous blinking of both button LEDs, with the yellow on running on background
	
# check if connected to the internet   
def is_connected():
  try: 
    # see if we can resolve the host name -- tells us if there is a DNS listening  
    host = socket.gethostbyname(config.test_server)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False    

# set variables to properly display the image on screen at right ratio
def set_demensions(img_w, img_h):
	# Note this only works when in booting in desktop mode. 
	# When running in terminal, the size is not correct (it displays small). Why?

    # connect to global vars
    global transform_y, transform_x, offset_y, offset_x

    # based on output screen resolution, calculate how to display
    ratio_h = (config.monitor_w * img_h) / img_w 

    if (ratio_h < config.monitor_h):
        #Use horizontal black bars
        #print "horizontal black bars"
        transform_y = ratio_h
        transform_x = config.monitor_w
        offset_y = (config.monitor_h - ratio_h) / 2
        offset_x = 0
    elif (ratio_h > config.monitor_h):
        #Use vertical black bars
        #print "vertical black bars"
        transform_x = (config.monitor_h * img_w) / img_h
        transform_y = config.monitor_h
        offset_x = (config.monitor_w - transform_x) / 2
        offset_y = 0
    else:
        #No need for black bars as photo ratio equals screen ratio
        #print "no black bars"
        transform_x = config.monitor_w
        transform_y = config.monitor_h
        offset_y = offset_x = 0

    # uncomment these lines to troubleshoot screen ratios
#     print str(img_w) + " x " + str(img_h)
#     print "ratio_h: "+ str(ratio_h)
#     print "transform_x: "+ str(transform_x)
#     print "transform_y: "+ str(transform_y)
#     print "offset_y: "+ str(offset_y)
#     print "offset_x: "+ str(offset_x)

# display one image on screen
def show_image(image_path):

	# clear the screen
	screen.fill( (0,0,0) )

	# load the image
	img = pygame.image.load(image_path)
	img = img.convert() 

	# set pixel dimensions based on image
	set_demensions(img.get_width(), img.get_height())

	# rescale the image to fit the current display
	img = pygame.transform.scale(img, (transform_x,transfrom_y))
	screen.blit(img,(offset_x,offset_y))
	pygame.display.flip()

# display a blank screen
def clear_screen():
	screen.fill( (0,0,0) )
	pygame.display.flip()

# display a group of images
def display_pics(png_group):
	for i in range(0, config.replay_cycles): # show pics a few times
		for i in range(1, total_pics+1): # show each pic
			show_image(config.file_path + png_group + "-0" + str(i) + ".png")
			time.sleep(config.replay_delay) # pause 

#Start the photobooth in gif making mode
def gifmode():
	yled.blink(on_time=0.3, off_time=0.3, n=5, background=False) # quick blink of yellow LED
	rled.off() # shut down the red LED
	make_gifs = True
	total_pics = config.gif_total_pics
	hi_res_pics = True
	print('Starting photobooth in gif mode')
	
#Start the photobooth in high defintion DSLR mode
def picmode():
	yled.off() # shut down the yellow LED
	rled.blink(on_time=0.3, off_time=0.3, n=5, background=False) # quick blink of red LED
	make_gifs = False
	total_pics = 1
	hi_res_pics = True
	print('Starting photobooth in DSLR mode')

# define the photo taking function for when a button is held long enough 
def start_photobooth(): 

	input(pygame.event.get()) # press escape to exit pygame. Then press ctrl-c to exit python.

	################################# Begin Step 1 #################################
	
	print('Get Ready') 
	yled.off() # shut down the yellow LED
	rled.off() # shut down the red LED
	show_image(real_path + "/instructions.png")
	sleep(config.prep_delay)
	
	# clear the screen
	clear_screen()
	
	camera = picamera.PiCamera()  
	camera.vflip = False
	camera.hflip = True # flip for preview, showing users a mirror image
	#camera.saturation = -100 # comment out this line if you want color images
	camera.iso = config.camera_iso
	
	pixel_width = 0 # local variable declaration
	pixel_height = 0 # local variable declaration
	
	if hi_res_pics:
		camera.resolution = (high_res_w, high_res_h) # set camera resolution to high res
	else:
		pixel_width = 500
		pixel_height = config.monitor_h * pixel_width // config.monitor_w
		camera.resolution = (pixel_width, pixel_height) # set camera resolution to low res
		
	################################# Begin Step 2 #################################
	
	print ('Taking pics')
	
	now = time.strftime("%Y-%m-%d-%H-%M-%S") #get the current date and time for the start of the filename

	if make_gifs:
		try: # take the photos
			for i in range(1,total_pics+1):
				camera.hflip = True # preview a mirror image
				camera.start_preview(resolution=(config.monitor_w, config.monitor_h)) # start preview at low res but the right ratio
				time.sleep(2) #warm up camera
				yled.on() #turn on the LED
				rled.on()
				filename = config.file_path + now + '-0' + str(i) + '.png'
				camera.hflip = False # flip back when taking photo
				camera.capture(filename,format='png',splitter_port=1)
				print(filename)
				time.sleep(config.capture_delay) # pause in-between shots
				yled.off()#turn off the LED
				rled.off()
				if i == total_pics+1:
					break
		finally:
			camera.stop_preview()
			camera.close()
	else: # DSLR capture case
		camera.hflip = True # preview a mirror image
		camera.start_preview(resolution=(config.monitor_w, config.monitor_h)) # start preview at low res but the right ratio
		#time.sleep(2)
		
		try: #take the DSLR photo
			yled.blink(on_time=0.2, off_time=0.2, n=10, background=True) # blink light to show users they can push the button
			rled.blink(on_time=0.2, off_time=0.2, n=10, background=False) # simultaneous blinking of both button LEDs
			yled.on() #turn on the LED
			rled.on()
			time.sleep(2) # to keep LEDs still before the shot
			filename = config.file_path + now + '.png'
			#picamera capture
			camera.hflip = False # flip back when taking photo
			camera.capture(filename,format='png',splitter_port=1)
			#DSLR capture
			#gpout = subprocess.check_output("gphoto2 --capture-image-and-download --filename filename", stderr=subprocess.STDOUT, shell=True) # https://github.com/safay/RPi_photobooth/blob/master/photo_booth.py
			#print(gpout)
			#if "ERROR" not in gpout: 
			#	snap += 1
			# Methode de binding à tester: https://github.com/jim-easterbrook/python-gphoto2#using-python-gphoto2
			# pour l'affichage avec prise en compte de l'alpha http://eoghan.me.uk/notes/2016/03/28/photo-booth/
			# ou ça http://picamera.readthedocs.io/en/release-1.10/recipes1.html#overlaying-images-on-the-preview
			print(filename)
			yled.off()#turn off the LED
			rled.off()
		finally:
			camera.stop_preview()
			camera.close()

	########################### Begin Step 3 #################################
	
	input(pygame.event.get()) # press escape to exit pygame. Then press ctrl-c to exit python.
	
	print('Creating an animated gif')
	
	if config.post_online:
		show_image(real_path + "/uploading.png")
	else:
		show_image(real_path + "/processing.png")
	
	if make_gifs: # make the gifs
		if hi_res_pics:
			# first make a small version of each image. Tumblr's max animated gif's are 500 pixels wide.
			for x in range(1, total_pics+1): #batch process all the images
				graphicsmagick = "gm convert -size 500x500 " + config.file_path + now + "-0" + str(x) + ".png -thumbnail 500x500 " + config.file_path + now + "-0" + str(x) + "-sm.png"
				os.system(graphicsmagick) #do the graphicsmagick action

			graphicsmagick = "gm convert -delay " + str(config.gif_delay) + " " + config.file_path + now + "*-sm.png " + config.file_path + now + ".gif" 
			os.system(graphicsmagick) #make the .gif
		else:
			# make an animated gif with the low resolution images
			graphicsmagick = "gm convert -delay " + str(config.gif_delay) + " " + config.file_path + now + "*.png " + config.file_path + now + ".gif" 
			os.system(graphicsmagick) #make the .gif

	########################### Begin Step 4 #################################
	
	input(pygame.event.get()) # press escape to exit pygame. Then press ctrl-c to exit python.
	
	try:
		display_pics(now)
	except Exception as e:
		tb = sys.exc_info()[2]
		traceback.print_exception(e.__class__, e, tb)
		pygame.quit()
		
	print('Done')
	
	if config.post_online:
		show_image(real_path + "/finished.png")
	else:
		show_image(real_path + "/finished2.png")
	
	time.sleep(config.restart_delay)
	show_image(real_path + "/intro.png")#;
	
	#yled.blink(on_time=1, off_time=1, n=None, background=True) # blink light to show users they can push the button
	#rled.blink(on_time=1, off_time=1, n=None, background=True) # simultaneous blinking of both button LEDs

####################
### Main Program ###
####################

## clear the previously stored pics based on config settings
if config.clear_on_startup:
	clear_pics(1)

print('Photo booth app running...')

yled.blink(on_time=0.5, off_time=0.5, n=5, background=True) # blink light to show the app is running
rled.blink(on_time=0.5, off_time=0.5, n=5, background=False) # simultaneous blinking of both button LEDs, with the yellow on running on background
	
show_image(real_path + "/intro.png")#;

make_gifs = False
total_pics = 1
hi_res_pics = True

while True:
	yled.blink(on_time=1, off_time=1, n=None, background=True) # blink light to show users they can push the button
	rled.blink(on_time=1, off_time=1, n=None, background=True) # simultaneous blinking of both button LEDs
	input(pygame.event.get()) # press escape to exit pygame. Then press ctrl-c to exit python.
	
	#ybutton.when_held = gifmode
	#rbutton.when_held = picmode

	rbutton.wait_for_press()
	
	start_photobooth()
