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
brightness = 1.0
resolution = 0.01
direction = 'asc'
pi.set_PWM_dutycycle(blueLed, 255*brightness)
while True:
    if direction == 'asc' and brightness == 1:
        direction = 'desc'
        logMessage('Changing to descending')
    if direction == 'desc' and brightness <= resolution:
        direction = 'asc'
        logMessage('Changing to ascending')
    
    if direction == 'asc':
        brightness += resolution
    else:
        brightness -= resolution
    
    # Apply new brightness
    pi.set_PWM_dutycycle(blueLed, 255*brightness)
    time.sleep(0.01)




#%%##############################
# Board cleanup
#################################
pi.stop()

