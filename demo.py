#!/usr/bin/env python

import time
from ws2812 import ws2812

color_chart = {
  'R': [ 100,   0,   0 ],
  'G': [   0, 100,   0 ],
  'B': [   0,   0, 100 ],
  'Y': [ 100, 100,   0 ],
  'P': [ 100,   0, 100 ],
  'C': [   0, 100, 100 ],
  'W': [ 100, 100, 100 ],
  ' ': [   0,   0,   0 ],
}

def read_graphic(filename):
  graphic = []

  fp = open(filename, "rb")

  for line in fp:
    graphic.append(line[:-1])

  fp.close()

  return graphic

def scroll_text(leds, text):
  width = len(text[0])
  red = 0
  green = 0
  blue = 100

  for i in range(0, width):
    leds.shift_left_8x5()

    for y in range(0, 5):
      #print str(i) + " " + str(y)
      if text[y][i] == ' ': value = 0
      else: value = 100

      leds.set_rgb((y * 8) + 7, 0, 0, value)

    leds.set_all_not_off(red, green, blue)
    red += 1
    blue -= 1
    leds.refresh()
    time.sleep(0.1)

  for i in range(0, 8):
    leds.shift_left_8x5()
    leds.set_all_not_off(red, green, blue)
    red += 1
    blue -= 1
    leds.refresh()
    time.sleep(0.1)

def draw_graphic(leds, graphic, x0, y0):
  width = len(graphic[0])
  height = len(graphic)

  #print str(width) + " " + str(height)

  for y in range(0, height):
    for x in range(0, width):
      #print str(x) + " " + str(y)
      pixel = graphic[y][x]

      if pixel not in color_chart: pixel = 'W'
      red = color_chart[pixel][0]
      green = color_chart[pixel][1]
      blue = color_chart[pixel][2]

      leds.set_rgb(((y + y0) * 8) + (x + x0), red, green, blue)

  leds.refresh()

def bounce_graphic(leds, graphic):
  width = len(graphic[0])
  height = len(graphic)
  red = 100
  green = 0
  blue = 50
  dr = -1
  dg = 1
  db = 1
  x = 1
  y = 0
  dx = 1
  dy = 1

  draw_graphic(leds, graphic, x, y)

  for count in range(0, 300):
    if count > 95:
      leds.set_all_not_off(red, green, blue)
      red += dr
      green += dg
      blue += db

      if red >= 100: dr = -1
      elif red < 0: dr = 1; red = 0

      if green >= 100: dg = -1
      elif green <= 0: dg = 1; green = 0

      if blue >= 100: db = -1
      elif blue <= 0: db = 1; blue = 0
    elif count > 50:
      leds.fade_out(2, 2, 2)

    if dx == 1: leds.shift_right_8x5(); x += 1
    else: leds.shift_left_8x5(); x -= 1
    if dy == 1: leds.shift_down_8x5(); y += 1
    else: leds.shift_up_8x5(); y -= 1

    if x == 8 - width: dx = -1
    elif x == 0: dx = 1
    if y == 5 - height: dy = -1
    elif y == 0: dy = 1

    leds.refresh()
    time.sleep(0.1)

  for i in range(0, 110):
    leds.fade_out(1, 1, 1)
    leds.refresh()
    time.sleep(0.05)

def draw_square(leds, x0, y0, width, height, red, green, blue):
  for x in range(x0, x0 + width):
    leds.set_rgb((y0 * 8) + x, red, green, blue)
    leds.set_rgb(((height + y0 - 1) * 8) + x, red, green, blue)

  for y in range(y0, y0 + height):
    leds.set_rgb((y * 8) + x0, red, green, blue)
    leds.set_rgb((y * 8) + width + x0 - 1, red, green, blue)

def draw_squares(leds):
  for i in color_chart:
    if i == ' ': continue
    x = 0
    y = 0
    width = 8
    height = 5

    red = color_chart[i][0]
    green = color_chart[i][1]
    blue = color_chart[i][2]

    while 1:
      leds.set_all(0, 0, 0)
      draw_square(leds, x, y, width, height, red, green, blue)
      leds.refresh()
      time.sleep(0.1)

      x += 1
      y += 1
      width -= 2
      height -= 2

      if height <= 0: break

def draw_fade(leds, r0, g0, b0, r1, g1, b1):
  dr = (r1 - r0) / 8
  dg = (g1 - g0) / 8
  db = (b1 - b0) / 8

  for i in range(0, 8):
    leds.set_rgb(i, r0, g0, b0)
    leds.set_rgb(i + 8, r0, g0, b0)
    leds.set_rgb(i + 16, r0, g0, b0)
    leds.set_rgb(i + 24, r0, g0, b0)
    leds.set_rgb(i + 32, r0, g0, b0)

    r0 += dr
    g0 += dg
    b0 += db

  leds.refresh()

def animate_fade(leds):

  draw_fade(leds, 100, 50, 0,  0, 100, 100)

  for i in range(0, 110):
    leds.fade_out(1, 1, 1)
    leds.refresh()
    time.sleep(0.05)

# ------------------------------- fold here ---------------------------------

leds = ws2812("/dev/ttyUSB0")

# Clear screen
leds.set_all(0, 0, 0)
leds.refresh()

# Scroll text
text = read_graphic("testing.txt")
scroll_text(leds, text)

# Load graphic
graphic = read_graphic("graphic.txt")
bounce_graphic(leds, graphic)

draw_squares(leds)

animate_fade(leds)

