import json
import datetime as dt
import time
import RPi.GPIO as GPIO



#%%##############################
# Initial setup
#################################
# Import config file
configFile = '/home/pi/Documents/Aquatronics/Source/Config.json'
CONFIG = json.loads(open(configFile,'r').read())



#%%##############################
# Helper functions
#################################

def logMessage(message):
    print('{}: {}'.format(dt.datetime.now(),message))
    # Send to log file as well



#%%##############################
# Board setup
#################################

# Set the board mode - BCM or BOARD
GPIO.setmode(GPIO.BOARD)

logMessage('GPIO mode: {}'.format(GPIO.getmode()))

# Disable warnings
GPIO.setwarnings(False)
logMessage('Warnings disabled')


blueLed = 37
GPIO.setup(blueLed,GPIO.OUT)

# Blinking LED
while True:
    GPIO.output(blueLed, True)
    logMessage('Blue LED On')
    time.sleep(0.5)
    GPIO.output(blueLed, False)
    logMessage('Blue LED Off')
    time.sleep(0.5)
    # To togle the output
#    GPIO.output(blueLed, not GPIO.input(blueLed))


# Chaning brightness of LED


# Dimming and brightening LED
# Uses PWM
pwmBlue = GPIO.PWM(blueLed, 1000)
pwmBlue.start(0)
brightness = 1
direction = 'asc'
while True:
    if direction == 'asc' and brightness == 100:
        direction = 'desc'
        logMessage('Changing to descending')
    if direction == 'desc' and brightness == 1:
        direction = 'asc'
        logMessage('Changing to ascending')
    
    if direction == 'asc':
        brightness += 1
    else:
        brightness -= 1
    
    # Apply new brightness
    pwmBlue.ChangeDutyCycle(brightness)
    time.sleep(0.05)




#%%##############################
# Board cleanup
#################################

GPIO.cleanup([blueLed])

