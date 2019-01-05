#!/usr/bin/python
#! -*- coding:utf-8 -*-
import time
import threading
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

level_pin = [[15,18,23,24],[12,16,20,21]]
GPIO.setup(level_pin, GPIO.IN)

def getWaterLevel():
  global level_pin
  level = [0] * 2
  
  while True:
    level[0] = 0
    for pin in level_pin[0]:
      level += not GPIO.input(pin)
    print(level)
    results[threading.current_thread().name] = level

def countRoundPerMinutes():
  while True:
    #--- sonic sensor  ---
    #--- you can do it ---
    
if __name__ == "__main__":
  
  while True:
    time.sleep(0.1)
    
      
