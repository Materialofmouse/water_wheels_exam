#!/usr/bin/python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

def pulseIn(PIN, start=1, end=0):
  if start==0: end = 1
  t_start = 0
  t_end = 0
  
  while GPIO.input(PIN) == end:
    t_start = time.time()                  
  while GPIO.input(PIN) == start:
    t_end = time.time()

  return t_end - t_start

def calc_distance(TRIG_PIN, ECHO_PIN, num, v=34000): 
  for i in range(num):
    GPIO.output(TRIG_PIN, GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    t = pulseIn(ECHO_PIN)
    distance = v * t/2
    print(distance, 'cm')
  GPIO.cleanup()

TRIG_PIN = 14
ECHO_PIN = 15
      

v = 33150 + 60*24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN,GPIO.OUT)
GPIO.setup(ECHO_PIN,GPIO.IN)
GPIO.setwarnings(False)

calc_distance(TRIG_PIN, ECHO_PIN, 100, v)
