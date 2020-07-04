# Simple test for NeoPixels on Raspberry Pi
import datetime as dt
import time
import math
import board
import neopixel


scheduleTime = ['08:00','08:30','10:00','10:10','18:45','19:00','19:30','19:45','20:00','22:00']
scheduleColour = [(0,0,0),(50,50,50),(50,50,50),(0,0,0),(0,0,0),(50,50,50),(50,12,10),(15,0,10),(0,0,10),(0,0,0)]


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 300

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

#pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)


def timeInRange(start, end, time):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= time <= end
    else:
        return start <= time or time <= end


def newColour(scheduleTime, scheduleColour, now):
    date = now.date()
    time = now.time()
    
    for i in range(len(scheduleTime)):
        if i == len(scheduleTime)-1:
            # Last time
            startTime = dt.datetime.strptime(scheduleTime[i], '%H:%M').time()
            endTime = dt.datetime.strptime(scheduleTime[0], '%H:%M').time()
            startColour = scheduleColour[i]
            endColour = scheduleColour[0]
        else:
            startTime = dt.datetime.strptime(scheduleTime[i], '%H:%M').time()
            endTime = dt.datetime.strptime(scheduleTime[i+1], '%H:%M').time()
            startColour = scheduleColour[i]
            endColour = scheduleColour[i+1]
            
        if timeInRange(startTime, endTime, time):
                    
            # Calculate the percentage through
                    
            startDateTime = dt.datetime.combine(date, startTime)
            endDateTime = dt.datetime.combine(date, endTime)
            
            if endDateTime < startDateTime:
                endDateTime = endDateTime + dt.timedelta(days=1)
            
            elapsed = (now-startDateTime).total_seconds()
            duration = (endDateTime-startDateTime).total_seconds()
            percentage = elapsed/duration
            r = math.ceil(startColour[0] + (endColour[0]-startColour[0])*percentage)
            g = math.ceil(startColour[1] + (endColour[1]-startColour[1])*percentage)
            b = math.ceil(startColour[2] + (endColour[2]-startColour[2])*percentage)
            print(startDateTime,endDateTime,startColour,endColour, (r,g,b))
            return ((r,g,b))


def colorWipe(pixels, color):
    """Wipe color across display a pixel at a time."""
    for i in range(pixels.n):
        pixels[i] = color
        pixels.show()


while True:
#    pixels.fill(newColour(scheduleTime, scheduleColour, dt.datetime.now()))
    colorWipe(pixels,newColour(scheduleTime, scheduleColour, dt.datetime.now()))
#    pixels.fill((50,50,0))
#    pixels.fill((50,12,10))
#    pixels.fill((15,0,10))
#    pixels.fill((0,0,10))
    pixels.show()
    time.sleep(10)
