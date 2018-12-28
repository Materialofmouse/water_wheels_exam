#!/usr/bin/python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import threading

class timer():
  def __init__(self):
    pass

  def check_write(self):
    while True:
      time.sleep(10)
  
  def check_rpm(self):
    while True:
      time.sleep(60)

class sensors():
  def __init__(self):
    level_pin = [18,23,24]

    GPIO.setwarnings(False)
    GPIO.setup(GPIO.BCM)
    GPIO.cleanup()

    #water sensor
    GPIO.setup(level_pin,GPIO.IN)

    #sonic sensor
    TRIG = 14
    ECHO = 15
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.OUT)

  def get_water_level(self):
    level = 0
    for i in range(self.level_pin):
      level += (not GPIO.input(i))

    return level

  def get_rpm(self):


