ws2812_driver
=============

Firmware for an attiny85 chip for controlling a WS2812 LED string over a UART

There are kind of two goals for this.  I got an 8x5 panel of these LED's
called an AdaFruit NeoPixel with an 8x5 grid of pixels:
(https://www.adafruit.com/products/1430).  A friend of mine got the same
WS2812 LED's on a string (30 of them).  The goal is to have some firmware
for an Atmel ATtiny85 that has drawing routines for both devices.

The concept works like this:  The ATtiny85 has 512 bytes of RAM.  120 of
these bytes are being used to hold 3 RGB values for 8 columns and 5 rows
of LED's.  The user can send a command over a soft-UART written for the
ATtiny85 to update the 24 bit color value of a pixel at any index in that
120 byte area.  For example if I want pixel 5 to be blue I can send 4 bytes:
0x05 0x00 0x00 0xff.  The data from the ATtiny85 isn't transferred to the
string of LED's until I send 0xff 0xff.  Therefore I can do all kinds of
drawing in RAM and nothing gets displayed until I'm ready.

If the first byte send to the soft-UART is an 0xff, then this means this is
a drawing command.  Drawing commands can be things like:  shift the entire
display of 8x5 pixels left by 1.  shift all pixels in the string right by
1, etc.  When drawing commands are being executed the soft-UART is being
ignored, so it's important to wait for a * char from the ATtiny85 to let
you know it's okay to send more data.  To make the whole thing easier there
is a Python library ws2812.py that can be used to send commands to the chip.

UART commands (all parameters are 1 byte):

index, r, g, b       Change pixel color at index
0xff, 0xff,          Refresh LED's with what currently is in RAM
0xff, 0xfe, r, g, b  Set all pixels to this color
0xff, 0xfd           Shift all pixels left (for string LEDS)
0xff, 0xfc           Shift all pixels right (for string LEDS)
0xff, 0xfb           Shift all pixels left (for 8x5 panel of LEDS) 
0xff, 0xfa           Shift all pixels right (for 8x5 panel of LEDS) 
0xff, 0xf9           Shift all pixels up (for 8x5 panel of LEDS) 
0xff, 0xf8           Shift all pixels down (for 8x5 panel of LEDS) 
0xff, 0xf7, r, g, b  Set all pixels that are not 0,0,0 to this value
0xff, 0xf6, r, g, b  Subtract this (r,g,b) vector from all pixels (fade out)
0xff, 0xf5, r, g, b  Add this (r,g,b) vector to all pixels (fade in?) 


