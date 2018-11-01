import os
import RPi.GPIO as gpio
import time
import random


POMP_UP   = 16
POMP_DOWN = 20

gpio.setmode(gpio.BCM)
gpio.setup(POMP_UP,gpio.OUT)
gpio.setup(POMP_DOWN,gpio.OUT)

gpio.output(POMP_UP,True)
gpio.output(POMP_DOWN,True)


def get():
  return random.choice([1,5,7,15,7])  

print('test program is running')

i = get()
print('reference level is ' + str(i))
a = int(input('input test:'))
print('check the now level...')

while True:
 
  if i == a:
    print('level control is done')
    gpio.cleanup()
    exit()

  elif a < i:
    gpio.output(16,False)
    a = a + 1
    
  else:
    gpio.output(20,False)
    a = a - 1

  time.sleep(1)
  print('level : ' + str(a))
  
