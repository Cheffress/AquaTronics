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


blueLed = 26
pi.set_mode(blueLed, pp.OUTPUT)

# Blinking LED
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

