#!/usr/bin/env python

import serial

class ws2812:
  def __init__(self, device):
    self.ser = serial.Serial(device, 9600)
    #print self.ser

  def close(self):
    self.ser.close()

  def refresh(self):
    self.ser.write(chr(0xff))
    self.ser.write(chr(0xff))
    self.ser.read(1)

  def set_rgb(self, index, r, g, b):
    self.ser.write(chr(index))
    self.ser.write(chr(r))
    self.ser.write(chr(g))
    self.ser.write(chr(b))
    self.ser.read(1)

  def set_all(self, r, g, b):
    self.ser.write(chr(0xff))
    self.ser.write(chr(0xfe))
    self.ser.write(chr(r))
    self.ser.write(chr(g))
    self.ser.write(chr(b))
    self.ser.read(1)

  def shift_left_linear(self):
    self.ser.write(chr(0xff))
    self.ser.write(chr(0xfd))
    self.ser.read(1)

  def shift_right_linear(self):
    self.ser.write(chr(0xff))
    self.ser.write(chr(0xfc))
    self.ser.read(1)

  def shift_left_8x5(self):
    self.ser.write(chr(0xff))
    self.ser.write(chr(0xfb))
    self.ser.read(1)

  def shift_right_8x5(self):
    self.ser.write(chr(0xff))
    self.ser.write(chr(0xfa))
    self.ser.read(1)

  def shift_up_8x5(self):
    self.ser.write(chr(0xff))
    self.ser.write(chr(0xf9))
    self.ser.read(1)

  def shift_down_8x5(self):
    self.ser.write(chr(0xff))
    self.ser.write(chr(0xf8))
    self.ser.read(1)

  def set_all_not_off(self,r,g,b):
    self.ser.write(chr(0xff))
    self.ser.write(chr(0xf7))
    self.ser.write(chr(r))
    self.ser.write(chr(g))
    self.ser.write(chr(b))
    self.ser.read(1)

  def fade_out(self,r,g,b):
    self.ser.write(chr(0xff))
    self.ser.write(chr(0xf6))
    self.ser.write(chr(r))
    self.ser.write(chr(g))
    self.ser.write(chr(b))
    self.ser.read(1)

  def fade_in(self,r,g,b):
    self.ser.write(chr(0xff))
    self.ser.write(chr(0xf5))
    self.ser.write(chr(r))
    self.ser.write(chr(g))
    self.ser.write(chr(b))
    self.ser.read(1)


