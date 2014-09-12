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

ser = serial.Serial("/dev/ttyUSB1", 9600)
print ser.name

#set_all(ser, 10, 30, 40)
set_rgb(ser, 20, 10, 30, 40)
refresh(ser)

ser.close()

