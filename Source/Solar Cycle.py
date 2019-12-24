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

piOutput = False
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
sleepCycle = CONFIG['intervalSeconds']
ledBrightness = CONFIG['led']['brightness']
brightnessRange = ledBrightness['max'] - ledBrightness['min']

# Set up the schedule
schedule = pd.DataFrame(CONFIG['schedule'])
schedule['time'] = pd.to_datetime(schedule['time'], format='%H:%M%:%S', errors='ignore')
endOfDay = pd.DataFrame([['23:59:59','000000']], columns=['time','colour'])
schedule = schedule.append(endOfDay)
schedule.sort_values(by='time')
schedule['time'] = pd.to_datetime(schedule['time'])


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

def rgbToHex(rgb):
    return '%02x%02x%02x' % rgb

def ledColour(schedule, ledBrightness, piOutput):
    '''Returns rgb values'''
    
    now = pd.to_datetime(dt.now())
    
    for i in range(1,len(schedule)):
        if now >= schedule.iloc[i-1,0] and now < schedule.iloc[i,0]:
            # Setup
            periodSeconds = (schedule.iloc[i,0]-schedule.iloc[i-1,0]).total_seconds()
            expiredSeconds = periodSeconds-(schedule.iloc[i,0]-now).total_seconds()
            expiredPercent = expiredSeconds/periodSeconds
            startRgb = hexToRgb(schedule.iloc[i-1,1])
            endRgb = hexToRgb(schedule.iloc[i,1])
            
            # Get r 8-bit value
            rEightBit = (startRgb[0]+(endRgb[0] - startRgb[0])*expiredPercent)
            gEightBit = (startRgb[1]+(endRgb[1] - startRgb[1])*expiredPercent)
            bEightBit = (startRgb[2]+(endRgb[2] - startRgb[2])*expiredPercent)
            # Convert r value to within brightness range
            r = math.ceil(rEightBit/255*brightnessRange)+ledBrightness['min']
            g = math.ceil(gEightBit/255*brightnessRange)+ledBrightness['min']
            b = math.ceil(bEightBit/255*brightnessRange)+ledBrightness['min']
            break
    
    if piOutput:
        return r, g, b
    else:
        return '#' + rgbToHex((math.ceil(rEightBit),math.ceil(gEightBit),math.ceil(bEightBit)))


def changeColours():
    colour=ledColour(schedule,ledBrightness,piOutput)
    window.configure(background=colour)
    window.after(1000, changeColours)


#%%##############################
# Window setup
#################################
if piOutput == False:
    window=tkinter.Tk()
    window.title('Light colour display')
    window.geometry('500x200')
    window.configure(background='black')
    window.after(100,changeColours)
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
    
    while 1 == 1:
        # Determine current colours
        r,g,b = ledColour(schedule, ledBrightness, piOutput)
        
        # R
        if r <= ledBrightness['min']:
            # Turn r off
            pi.write(redLed, False)
        else:
            pi.write(redLed, True)
            pi.set_PWM_dutycycle(redLed, r)
        # G
        if g <= ledBrightness['min']:
            # Turn r off
            pi.write(greenLed, False)
        else:
            pi.write(greenLed, True)
            pi.set_PWM_dutycycle(greenLed, g)
        # B
        if b <= ledBrightness['min']:
            # Turn r off
            pi.write(blueLed, False)
        else:
            pi.write(blueLed, True)
            pi.set_PWM_dutycycle(blueLed, b)

        # Pause for n seconds
        time.sleep(1)



#%%##############################
# Board cleanup
#################################
if piOutput:
    pi.stop()

