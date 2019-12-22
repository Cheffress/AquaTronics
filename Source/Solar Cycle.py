import json
import datetime as dt
import time
import pigpio as pp

# Must run below prior to running code
# sudo pigpiod


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

# Connects to local RPi
pi = pp.pi()

redLed = 17
greenLed = 11
blueLed = 26
pi.set_mode(redLed, pp.OUTPUT)
pi.set_mode(greenLed, pp.OUTPUT)
pi.set_mode(blueLed, pp.OUTPUT)


pi.write(redLed, True)
pi.write(redLed, False)
pi.write(greenLed, True)
pi.write(greenLed, False)
pi.write(blueLed, True)
pi.write(blueLed, False)


# Blinking LED
if False:
    while True:
        pi.write(blueLed, True)
        logMessage('Blue LED On')
        time.sleep(0.5)
        pi.write(blueLed, False)
        logMessage('Blue LED Off')
        time.sleep(0.5)


# Chaning brightness of LED


# Dimming and brightening LED
# Uses PWM
maxBrightness = 100
minBrightness = 7
brightness = 100
resolution = 1
sleepCycle = 1
direction = 'asc'
while True:
    if direction == 'asc' and brightness == maxBrightness:
        direction = 'desc'
        logMessage('Changing to descending')
    if direction == 'desc' and brightness <= minBrightness:
        direction = 'asc'
        logMessage('Changing to ascending')
    
    if direction == 'asc':
        brightness += resolution
    else:
        brightness -= resolution
    
    # Apply new brightness
    print(brightness)
    pi.set_PWM_dutycycle(redLed, brightness)
    pi.set_PWM_dutycycle(greenLed, brightness)
    pi.set_PWM_dutycycle(blueLed, brightness)
    time.sleep(sleepCycle)



#%%##############################
# Board cleanup
#################################
pi.stop()

