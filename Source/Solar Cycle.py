#%%#########################################
# Notes
############################################
# Create graph of colours throughout the day every 10 minutes




#%%##############################
# Import modules
#################################

import json
import datetime as dt
import time
import pigpio as pp
import tkinter
import pandas as pd
import os
from datetime import datetime as dt
import math

piOutput = True
host = 'pc'
configFile = 'Config.json'

rValue = 0
gValue = 0
bValue = 0
# Must run below prior to running code
# sudo pigpiod


#%%##############################
# Initial setup
#################################
# Set curent working directory
if host == 'pi':
    homeDir = '/home/pi/Documents/Aquatronics/Source'
else:
    homeDir = 'E:/Git/Aquatronics/Source'

os.chdir(homeDir)

# Import config file
CONFIG = json.loads(open(configFile,'r').read())


#%%##############################
# General setup
#################################
maxBrightness = CONFIG['led']['brightness']['max']
minBrightness = CONFIG['led']['brightness']['min']
resolution = CONFIG['led']['brightness']['resolution']
sleepCycle = CONFIG['intervalSeconds']
#schedule = CONFIG['schedule']


#%%##############################
# Helper functions
#################################

def logMessage(message):
    print('{}: {}'.format(dt.datetime.now(),message))
    # Send to log file as well


def readJson(fileName):
    '''Import JSON file'''
    json_output = json.loads(open(fileName,'r').read())
    return json_output

def timeInRange(start, end, x):
    '''Return true if x is in the range [start, end]'''
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def hexToRgb(h):
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def ledColour(schedule,ledBrightness):
    '''Returns rgb values'''
    now = pd.to_datetime(dt.now())
    
    
    r=1
    g=2
    b=3
    return r, g, b

#r,g,b = ledColour(schedule,CONFIG['led'])







ledBrightness = CONFIG['led']['brightness']
schedule = CONFIG['schedule']
brightnessRange = ledBrightness['max'] - ledBrightness['min']

schedule = pd.DataFrame(schedule)
schedule['time'] = pd.to_datetime(schedule['time'], format='%H:%M%:%S', errors='ignore')
endOfDay = pd.DataFrame([['23:59:59','000000']], columns=['time','colour'])
schedule = schedule.append(endOfDay)
schedule.sort_values(by='time')
schedule['time'] = pd.to_datetime(schedule['time'])

now = pd.to_datetime(dt.now())

for i in range(1,len(schedule)):
    if now >= schedule.iloc[i-1,0] and now < schedule.iloc[i,0]:
        print(schedule.iloc[i-1,0],schedule.iloc[i,0])
        periodSeconds = (schedule.iloc[i,0]-schedule.iloc[i-1,0]).total_seconds()
        expiredSeconds = periodSeconds-(schedule.iloc[i,0]-now).total_seconds()
        expiredPercent = expiredSeconds/periodSeconds
        startRgb = hexToRgb(schedule.iloc[i-1,1])
        endRgb = hexToRgb(schedule.iloc[i,1])
        
        
        r = (abs(endRgb[0] - startRgb[0])/255 / ledBrightness['max'] * brightnessRange)+ledBrightness['min']
        # Get r value
        r = (startRgb[0]+(endRgb[0] - startRgb[0])*expiredPercent)
        # Convert r value to within range
        r = math.ceil(r/255*ledBrightness['max'])
        
        
        
        if startRgb <> endRgb:
        
        
        
        if r <= ledBrightness['min']:
            # Turn r off
            pi.write(redLed, False)
        else:
            pi.write(redLed, True)
        
        
        
        print(periodSeconds,expiredSeconds,expiredPercent)
        break
        
    



#%%##############################
# Window setup
#################################
if piOutput == False:
    window=tkinter.Tk()
    window.title('Light colour display')
    window.geometry('500x200')
    window.configure(background='black')
    window.mainloop()
    



#%%##############################
# Board setup
#################################

if piOutput:
    # Connects to local RPi
    pi = pp.pi()
    
    # Allocate pins and set mode
    redLed = CONFIG['led']['pins']['r']
    greenLed = CONFIG['led']['pins']['g']
    blueLed = CONFIG['led']['pins']['b']
    pi.set_mode(redLed, pp.OUTPUT)
    pi.set_mode(greenLed, pp.OUTPUT)
    pi.set_mode(blueLed, pp.OUTPUT)
    
    
    # Dimming and brightening LED
    brightness = 0

    pi.set_PWM_dutycycle(redLed, brightness)
    pi.set_PWM_dutycycle(greenLed, brightness)
    pi.set_PWM_dutycycle(blueLed, brightness)
    time.sleep(sleepCycle)



#%%##############################
# Board cleanup
#################################
if piOutput:
    pi.stop()

