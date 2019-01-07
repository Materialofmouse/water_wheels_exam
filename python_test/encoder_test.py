import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

GPIO.setup(17,GPIO.IN)
flag = True
cnt = 0

try:
  t = int(time.strftime('%S'))
  while not (int(time.strftime('%S')) - t == 10):
    if GPIO.input(17) == True and flag == True:
      flag = False
      cnt += 1
    
    elif GPIO.input(17) == False:
      flag = True

  print(cnt)
except KeyboardInterrupt:
  print(cnt)
