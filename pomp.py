import RPi.GPIO as gpio
import time

POMP_UP   = 16
POMP_DOWN = 20

gpio.setmode(gpio.BCM)
gpio.setup(POMP_UP,gpio.OUT)
gpio.setup(POMP_DOWN,gpio.OUT)


#water level up
def pomp_up(sec):
  gpio.output(POMP_UP,False)
  time.sleep(sec)
  return gpio.output(POMP_UP,True)

##water level down
def pomp_down(sec):
  gpio.output(POMP_DOWN,False)
  time.sleep(sec)
  return gpio.output(POMP_DOWN,True)

while True:
  pomp_up(0.5)
  pomp_down(0.5)
