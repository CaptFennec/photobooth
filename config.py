# Tumblr Setup removed

#Config settings to change behavior of photo booth
monitor_w = 800    # width of the display monitor
monitor_h = 600    # height of the display monitor
file_path = '/home/pi/photobooth/pics/' # path to save images
clear_on_startup = False # True will clear previously stored photos as the program launches. False will leave all previous photos.
post_online = False # True to upload images. False to store locally only.
capture_count_pics = False # if true, show a photo count between taking photos. If false, do not. False is faster.
#make_gifs = False   # True to make an animated gif. False to post 4 jpgs into one post.
#hi_res_pics = True  # True to save high res pics from camera.
                    # If also uploading, the program will also convert each image to a smaller image before making the gif.
                    # False to first capture low res pics. False is faster.
                    # Careful, each photo costs against your daily Tumblr upload max.
camera_iso = 800    # adjust for lighting issues. Normal is 100 or 200. Sort of dark is 400. Dark is 800 max.
                    # available options: 100, 200, 320, 400, 500, 640, 800
gif_total_pics = 3 # number of pictures to be taken to make the gifs
capture_delay = 1 # delay between pics (seconds?)
prep_delay = 5 # number of seconds at step 1 as users prep to have photo taken
gif_delay = 100 # How much time between frames in the animated gif (ms?)
restart_delay = 10 # how long to display finished message before beginning a new session (seconds?)
test_server = 'www.google.com'
replay_delay = 1 # how much to wait in-between showing pics on-screen after taking
replay_cycles = 2 # how many times to show each photo on-screen after taking
