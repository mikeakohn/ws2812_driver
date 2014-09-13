ws2812_driver
=============

Firmware for an attiny85 chip for controlling a WS2812 LED string over a UART

UART commands (all parameters are 1 byte):

index, r, g, b       Change pixel color at index
0xff, 0xff,          Refresh LED's with what currently is in RAM
0xff, 0xfe, r, g, b  Set all pixels to this color
0xff, 0xfd           Shift all pixels left (for string LEDS)
0xff, 0xfc           Shift all pixels right (for string LEDS)


