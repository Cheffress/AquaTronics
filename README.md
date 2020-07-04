# AquaTronics

**A lighting simlation script for your aquarium**

A basic python script which controls addressable-RGB leds (WS2812B) to simulate sunrise/sunset lighting.  This script doesn't only adjust brightness, but also the colour, allowing a sunset to realistically fade from white, to yellow to orange to red, or whatever colours you choose.  This is achieved by setting multiple time-of-day/colour combinations and the script will calculate the interim colour at any point in time.

E.g. if input were

Time R,B,G

10AM 100,50,20

11AM 200,200,200


then the colours at 10:30 would be 150,125,110 (RGB).

I hope this can be useful for simulating the solar cycle in your aquarium.
