# -*- coding: utf-8 -*-

import picamera
import RPi.GPIO as GPIO
import time # For time-stamp



## ----------------------------------------------------------------------------
## Set path and filename with time-stamp
timestr = time.strftime("%d-%m-%Y_%H-%M-%S")
path = 'home/pi/Desktop/'
filename = 'pic_'+timestr+'.jpg'

## TO-DO remove gipo map
#gpio17=11
#gpio18=13
#gpio22=15
#gpio23=16
#gpio27=12

##Set GPIO numbering system
GPIO.setmode(GPIO.BCM)

##Set GPIO numbers for shutter and LEDs
gpio_SHUTTER=17
gpio_IR_LED=22
gpio_WH_LED=23

## Turn down warnings if ports are accidentally remained occupied during
## a previous instance of the program
#GPIO.setwarnings(False)


try:
    ## GPIO 17 is the shutter button
    GPIO.setup(gpio_SHUTTER, GPIO.IN, GPIO.PUD_UP)

    ## GPIO 22 is the infrared cathode
    GPIO.setup(gpio_IR_LED, GPIO.OUT)

    ## GPIO 23 is the white light cathode
    GPIO.setup(gpio_WH_LED, GPIO.OUT)

    ## Sets the infrared cathode to ground. The common anode of the
    ## LED is set to 3.3 V, so setting GPIO 22 to ground causes the
    ## infrared light to be on.
    GPIO.output(gpio_IR_LED, False)

    ## Sets the white light cathode to 3.3 V
    GPIO.output(gpio_WH_LED, True)
except:
    ## Catch possible errors
    print('ERROR: Failed to set GPIOs. Exiting')
    raise SystemExit


with picamera.PiCamera() as camera:
    camera.start_preview()
    try:
        camera.start_preview()
        GPIO.wait_for_edge(17, GPIO.FALLING)
        GPIO.output(gpio_IR_LED, True)
        GPIO.output(gpio_WH_LED, False)
        camera.capture(path+filename, use_video_port=True)
    finally:
        camera.stop_preview()
        ## Clean GPIO ports previously set in this program
        GPIO.cleanup()





## Notes (TO-DO delete)

## For rotating the image and changing brightness
# camera.vflip = True
# camera.hflip = True
# camera.brightness = 60  ## Add brightness handle?
