from picamera import PiCamera
from gpiozero import Button
from overlay_functions import *
from time import gmtime, strftime

# Tell the next overlay button what to do
def next_overlay():
    global overlay
    overlay = next(all_overlays)
    preview_overlay(camera, overlay)
    
    #if 'overlay' in globals():
    #    overlay = next(all_overlays)
    #else:
    #    global overlay # http://stackoverflow.com/questions/843277/how-do-i-check-if-a-variable-exists
    #    overlay = next(all_overlays)# http://stackoverflow.com/questions/26545051/is-there-a-way-to-delete-created-variables-functions-etc-from-the-memory-of-th
    #preview_overlay(camera, overlay)

# Tell the take picture button what to do
def take_picture():
    camera.capture(output)
    camera.stop_preview()

# Set up buttons
next_overlay_btn = Button(23)
next_overlay_btn.when_pressed = next_overlay
take_pic_btn = Button(25)
take_pic_btn.when_pressed = take_picture

# Set up camera (with resolution of the touchscreen)
camera = PiCamera()
camera.resolution = (800, 480)
camera.hflip = True

# Start camera preview (delete alpha=128 once you know your code works)
camera.start_preview(alpha=128)

# Set up filename
output = strftime("/home/pi/photobooth/tests/allseeingpi_test/image-%d-%m %H:%M.png", gmtime())
