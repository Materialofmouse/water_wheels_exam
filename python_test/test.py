import time
import RPi.GPIO as gpio

setmode(gpio.BCM)
setup(16,gpio.OUT)
setup(20,gpio.OUT)

while True:
  gpio.output(16,True)
  gpio.output(20,False)
  time.sleep(1)
  gpio.output(16,False)
  gpio.output(20,True)
  time.sleep(1)
