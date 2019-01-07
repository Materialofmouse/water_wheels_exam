import threading
import queue
import RPi.GPIO as GPIO
import time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

level_pin = [[15,18,23,24],[12,16,20,21]]
GPIO.setup(level_pin[0], GPIO.IN)
GPIO.setup(level_pin[1], GPIO.IN)

q = queue.Queue()

def set_water_level():
  global level_pin
  level = [0] * 2
  
  for i,pin_num in enumerate(level_pin):
    for pin in pin_num:
      level[i] += not GPIO.input(pin)
   
  global q
  q.put(dict(level1=level[0] + 1, level2=level[1] + 1))
  print('[level] --- ok')

def set_water_temp():
  import subprocess
  #--- get water level ---
  global q
  t = subprocess.check_output(['cat','/sys/class/hwmon/hwmon0/temp1_input'])
  q.put(dict(temp = t))
  print('[temp]  --- ok')

def rpm_get():
  

def main():
  import os
  from datetime import datetime
  import pytz
  import csv


  JST = pytz.timezone('Asia/Tokyo')
  filepath = str('/home/pi/data/' + str(datetime.now(JST).strftime('%Y/%m/%d')))

  if not (os.path.isdir(filepath)):
    os.makedirs(filepath)
  writepath = filepath + '/' + str(datetime.now(JST).strftime('%H:%M:%S')) + '.csv'

  while True:
    threadlist = list()
    threadlist.append(threading.Thread(target=set_water_level()))
    threadlist.append(threading.Thread(target=set_water_temp()))
    threadlist.append(threading.Thread(target=on_timer()))
    threadlist.append(threading.Thread(target=test_timer()))

    for thread in threadlist:
      thread.start()

    for thread in threadlist:
      thread.join()
    
    data = q.get()
    while not q.empty():
      data.update(q.get())
    
    print(data)
    f = open(writepath,'a')
    writer = csv.writer(f,lineterminator='\n')

    writedata = []
    writedata.append(str(datetime.now(JST).strftime('%H:%M:%S')))
    writedata.append(str(data['temp']))
    writedata.append(str(data['level1']))
    writedata.append(str(data['level2']))

    writer.writerow(writedata)
    f.close()

  ## --- kaki komi syori ---

if __name__ == '__main__':
  main()
