import picamera
from time import sleep
import time
import RPi.GPIO as GPIO
from os import system
import os
import random, string

########################
#
# Behaviour Variables
#
########################

shortTake = 12 # defines frames in a short gif
longTake = 24 # defines frames in a long GIF
num_frame = 0  # stores number of frames to be captured (will be defined by short ot long take)
gif_delay = 10  # frame delay [ms]
rebound = False  # create a GIF that loops start <=> end

########################
#
# Define GPIO
#
########################

GPIO.setmode(GPIO.BCM) #Set the GPIO pin reference to GPIO numbering
GPIO.setwarnings(False) #Not sure what this does , but do it!

shutterButton = 20 #Define GPIO pin attached to the shutter button
GPIO.setup(shutterButton, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Set shutter pin as input and pull it up

# Note on LEDs: make sure pins support PWM if you want them to blink

led_1 = 12 #Define the GPIO pin attached to the LED want to indicate you are recording (pointed towards subject)
GPIO.setup(led_1, GPIO.OUT) #Set pin to output
recordingLed = GPIO.PWM(led_1, 2) #set pin up PWM control

led_2 = 25 #Define the  GPIO pin attached to the LED you want to indicate ready, recording, and processing (pointed towards operator)
GPIO.setup(led_2, GPIO.OUT) #Set pin to output
statusLed = GPIO.PWM(led_2, 2) #set pin up for PWM control

led_3 = 16 #Define the  GPIO pin attached to the LED in the shutter button
GPIO.setup(led_3, GPIO.OUT) #Set pin to output
buttonLed = GPIO.PWM(led_3, 2) #set pin up for PWM control

switch_1 = 26 #Define the GPIO pin attached to a switch to control on  of the camera features
GPIO.setup(switch_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
lengthSwitch = switch_1 #Define the switch that will control the number of frames captured

switch_2 =  19 #Define the GPIO pin attached to a switch to control on  of the camera features
GPIO.setup(switch_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
reboundSwitch = switch_2 #Define the frame that controls if the GIF will rebound

switch_3 =  13 #Define the GPIO pin attached to a switch to control on  of the camera features
GPIO.setup(switch_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
effectSwitch = switch_3 #Define the switch that will control if a funky effect will be applied or not

switch_4 = 6 #Define the GPIO pin attached to a switch to control on  of the camera features
GPIO.setup(switch_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
styleSwitch = switch_4 #Define the swith that selects the effect (camera.effect)


########################
#
# Camera
#
########################

camera = picamera.PiCamera()
camera.resolution = (540, 405)
camera.rotation = 90
#camera.brightness = 70

########################
#
# Capture  loop
#
########################

# Indicate ready status
statusLed.start(100)
buttonLed.start(100)
recordingLed.start(100)
print('System Ready')

#Random number function to append to file name function for file name
def random_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

#Main code

try:
    while True:
        if GPIO.input(shutterButton) == False: # Detect if shutter is pressed

            ### TAKING PICTURES ###

            print('Gif Started')
	    print(rebound)
	    print(num_frame)
	    print(camera.image_effect)

            statusLed.ChangeDutyCycle(50) # make LED blink while recording (50 means blink)
	    buttonLed.ChangeDutyCycle(50) 
            recordingLed.ChangeDutyCycle(100) #turn LED on while recording (100 = on)

            randomstring = random_generator()
            for i in range(num_frame):
                camera.capture('{0:04d}.jpg'.format(i))

            ### PROCESSING GIF ###
            print('processing 1')
            statusLed.ChangeFrequency(6) # changing freq. changes blink speed, status light blinks faster  while processing (bigger number = faster blinks)
            recordingLed.ChangeDutyCycle(0) # turns LED off (0 = off)
	    buttonLed.ChangeDutyCycle(0)
            if rebound == True: # make copy of images in reverse order
                for i in range(num_frame - 1):
                    source = str(num_frame - i - 1) + ".jpg"
                    source = source.zfill(8) # pad with zeros
                    dest = str(num_frame + i) + ".jpg"
                    dest = dest.zfill(8) # pad with zeros
                    copyCommand = "cp " + source + " " + dest
                    os.system(copyCommand)

            filename = '/home/pi/gifcam/gifs/' + randomstring + '-0'
            print('Processing 2')
            graphicsmagick = "gm convert -delay " + str(gif_delay) + " " + "*.jpg " + filename + ".gif" 
            os.system(graphicsmagick)
            os.system("rm ./*.jpg") # cleanup source images

            print('Done')
            print('System Ready')

        else : # Button NOT pressed
            ### READY TO MAKE GIF ###
            # print('end')

            statusLed.ChangeFrequency(2) # resets the freq. for normal blinking
            statusLed.ChangeDutyCycle(100) # turns led on (100 = 0n) Indicates camera is ready to shoot again 
	    buttonLed.ChangeDutyCycle(100)
            recordingLed.ChangeDutyCycle(0)

	    # enable these to test switches
	    # print(rebound)
	    # print(num_frame)
	    # print(camera.image_effect)

	    ### CHECK STATE OF HARDWARE SWITCHES ###

            if GPIO.input(reboundSwitch) == True : # check rebound switch
            	rebound = True
            if GPIO.input(reboundSwitch) == False :
		rebound = False

	    if GPIO.input(lengthSwitch) == True : # check shot length switch
		num_frame = longTake
	    else :
	    	num_frame = shortTake

	    if  GPIO.input(effectSwitch) == True : # check if effect switch is on
		if GPIO.input(styleSwitch) == True : # if on, read last switch to pick effect 
	    		camera.image_effect = 'colorswap'
	        else :
			camera.image_effect = 'solarize' # you can swap these effects for others, look up the PiCamera.IMAGE_EFFECTS documentation
	    else :
		if GPIO.input(styleSwitch) == True : #If the effect switch is off the style switch toggles between no effect and film grain
			camera.image_effect= 'film'
		else :
			camera.image_effect = 'none'

            sleep(0.05)

except:
    GPIO.cleanup()
