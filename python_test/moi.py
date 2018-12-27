#!/use/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep

level_pin = [18,23,24]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

GPIO.setup(level_pin, GPIO.IN)


while True:
  level = not GPIO.input(18)
  level += (not GPIO.input(23))
  level += (not GPIO.input(24))
  print(level)
  sleep(0.1)
