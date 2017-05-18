#!/usr/bin/env python

from time import sleep
from gpiozero import LED, Button
import atexit
from signal import pause

########################
### Variables Config ###
########################

yled = LED(27) # pin definition for yellow button LED, active high (GPIO-resistor-long_LED_short-GND), off by default
rled = LED(23) # pin definition for red button LED, active high (GPIO-resistor-long_LED_short-GND), off by default

#ybutton = Button(22, pull_up=True, bounce_time=0.3, hold_time=3, hold_repeat=False) # pin definition for yellow button
#rbutton = Button(24, pull_up=True, bounce_time=0.3, hold_time=3, hold_repeat=False) # pin definition for red button

ybutton = Button(22, bounce_time=0.3, hold_time=2) # pin definition for yellow button
rbutton = Button(24, bounce_time=0.3, hold_time=2) # pin definition for red button

#################
### Functions ###
#################

def cleanup():
  yled.off()
  rled.off()
  print('Goodbye.')
atexit.register(cleanup) 

#Start the photobooth in gif making mode
def gifmode():
	rled.off() # shut down the red LED
	yled.blink(on_time=0.3, off_time=0.3, n=5, background=False) # quick blink of yellow LED
	make_gifs = True
	print('Setting photobooth in gif mode')
	
	start_photobooth()
	
#Start the photobooth in high defintion DSLR mode
def picmode():
	yled.off() # shut down the yellow LED
	rled.blink(on_time=0.3, off_time=0.3, n=5, background=False) # quick blink of red LED
	make_gifs = False
	print('Setting photobooth in DSLR mode')
	
	start_photobooth()

# define the photo taking function for when a button is held long enough 
def start_photobooth(): 

	################################# Begin Step 1 #################################
	
	if make_gifs:
		print('Photo booth launched in gif mode')
	else:
		print('Photo booth launched in DSLR mode')
	yled.off() # shut down the yellow LED
	rled.off() # shut down the red LED

####################
### Main Program ###
####################

print('Photo booth app running...')

sleep(5)

yled.blink(on_time=0.5, off_time=0.5, n=5, background=True) # blink light to show the app is running
rled.blink(on_time=0.5, off_time=0.5, n=5, background=False) # simultaneous blinking of both button LEDs, with the yellow on running on background
	
make_gifs = False

yled.blink(on_time=1, off_time=1, n=None, background=True) # blink light to show users they can push the button
rled.blink(on_time=1, off_time=1, n=None, background=True) # simultaneous blinking of both button LEDs

while True:
	try:
		if ybutton.is_held:
			print('Bouton jaune maintenu')
			gifmode()
		if rbutton.is_held:
			print('Bouton rouge maintenu')
			picmode()
	except KeyboardInterrupt:
		cleanup()

# try:
	# ybutton.when_held = gifmode
	# rbutton.when_held = picmode
	# pause()
# except KeyboardInterrupt:
	# cleanup()
