#!/usr/bin/env python

import serial

def refresh(ser):
  ser.write(chr(0xff))
  ser.write(chr(0xff))
  print ser.read(1)

def set_rgb(ser, index, r, g, b):
  ser.write(chr(index))
  ser.write(chr(r))
  ser.write(chr(g))
  ser.write(chr(b))
  print ser.read(1)

def set_all(ser, r, g, b):
  ser.write(chr(0xff))
  ser.write(chr(0xfe))
  ser.write(chr(r))
  ser.write(chr(g))
  ser.write(chr(b))
  print ser.read(1)

# --------------------------------- fold here -----------------------------

ser = serial.Serial("/dev/ttyUSB0", 9600)
print ser.name

set_all(ser, 0, 0, 0)
set_rgb(ser, 18, 0, 0, 0)
set_rgb(ser, 19, 40, 30, 100)
set_rgb(ser, 21, 100, 0, 0)
set_rgb(ser, 22, 0, 100, 0)

refresh(ser)

ser.close()

