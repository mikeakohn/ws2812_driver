#!/usr/bin/env python

import time
from ws2812 import ws2812

def read_scroll_text(filename):
  text = []

  fp = open(filename, "rb")

  for line in fp:
    text.append(line[:-1])

  fp.close()

  return text

def scroll_text(leds, text):
  text_len = len(text[0])

  for i in range(0, text_len):
    leds.shift_left_8x5()

    for y in range(0, 5):
      print str(i) + " " + str(y)
      if text[y][i] == ' ': value = 0
      else: value = 100

      leds.set_rgb((y * 8) + 7, 0, 0, value)

    leds.refresh()
    time.sleep(0.1)

  for i in range(0, 8):
    leds.shift_left_8x5()
    leds.refresh()
    time.sleep(0.1)

# ------------------------------- fold here ---------------------------------

leds = ws2812("/dev/ttyUSB0")

# Clear screen
leds.set_all(0, 0, 0)
leds.refresh()

# Scroll text
text = read_scroll_text("testing.txt")

print text

scroll_text(leds, text)


