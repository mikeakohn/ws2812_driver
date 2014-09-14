#!/usr/bin/env python

import time
from ws2812 import ws2812

leds = ws2812("/dev/ttyUSB0")

#ser = serial.Serial("/dev/ttyUSB0", 9600)

leds.set_all(0, 0, 10)
leds.refresh()
time.sleep(1)

leds.set_all(0, 0, 0)
leds.set_rgb(2, 100, 0, 0)
leds.set_rgb(22, 0, 100, 0)
leds.refresh()
time.sleep(1)

for i in range(0, 3):
  leds.shift_right_linear()
  leds.refresh()
  time.sleep(1)

for i in range(0, 10):
  leds.shift_left_linear()
  leds.refresh()
  time.sleep(1)

for i in range(0, 5): leds.set_rgb(4 + i * 8, 0, 0, 100)
leds.refresh()

for i in range(0, 10):
  leds.shift_left_8x5()
  leds.refresh()
  time.sleep(1)

for i in range(0, 5): leds.set_rgb(4 + i * 8, 0, 100, 0)
leds.refresh()

for i in range(0, 5):
  leds.shift_right_8x5()
  leds.refresh()
  time.sleep(1)

leds.set_all(0, 0, 100)
leds.refresh()

for i in range(0, 3):
  leds.shift_up_8x5()
  leds.refresh()
  time.sleep(1)

leds.set_all(100, 0, 0)
leds.refresh()

for i in range(0, 3):
  leds.shift_down_8x5()
  leds.refresh()
  time.sleep(1)

leds.set_all_not_off(0,0,100)
leds.refresh()
time.sleep(1)

leds.fade_out(50,0,50)
leds.refresh()
time.sleep(1)

leds.fade_out(50,0,60)
leds.refresh()
time.sleep(1)

for i in range(10, 20): leds.set_rgb(i, 40, 30, 100)
leds.refresh()
time.sleep(1)

for i in range(0, 10):
  leds.fade_in(10,4,7)
  leds.refresh()
  time.sleep(1)

leds.set_all(0, 0, 0)
leds.refresh()

