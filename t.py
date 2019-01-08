import threading
import queue
import RPi.GPIO as GPIO
import Adafruit_DHT as DHT
import time
import sys
from datetime import datetime
import subprocess
import os
import pytz
import csv

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

LEVEL_PIN = [[15,18,23,24],[12,16,20,21]]
RPM_PIN = [17,27]

GPIO.setup(LEVEL_PIN[0], GPIO.IN)
GPIO.setup(LEVEL_PIN[1], GPIO.IN)
GPIO.setup(RPM_PIN,GPIO.IN)

WATER_TEMP_PATH = '/sys/class/hwmon/hwmon0/'

q = queue.Queue()

def put_water_level():
  print('[level]  --- start')
  level = [0] * 2
  
  for i,pin_num in enumerate(LEVEL_PIN):
    for pin in pin_num:
      level[i] += not GPIO.input(pin)
   
  q.put(dict(level1=level[0] + 1, level2=level[1] + 1))
  print('[level]  --- ok')


def put_temp():
  #--- get water level ---
  key = ['temp','temp1','temp2','temp3']
  t = []
  
  SENSOR = DHT.DHT11
  DHT_PIN = 22
  print('[temp]   --- start')
  h,temp = DHT.read_retry(SENSOR,DHT_PIN)
  t.append(temp)
  print('[temp]   --- ok')
  for i in range(1):
    print('[temp' + str(i + 1) + ']  --- start')
    t.append(float(subprocess.check_output(['cat',WATER_TEMP_PATH + 'temp' + str(i + 1) + '_input'])) / 1000)
    print('[temp' + str(i + 1) + ']  --- ok')
  d = dict(zip(key, t))
  q.put(d)


def rpm_get(pin_num):
  start_time = datetime.now()
  cnt = 0
  flag = True
  print('[rpm' + str(pin_num + 1) +']   --- start')
  
  while not (datetime.now() - start_time).seconds == 10:
    if GPIO.input(RPM_PIN[pin_num]) == True and flag == True:
      flag = False
      cnt += 1
    elif GPIO.input(RPM_PIN[pin_num]) == False:
      flag = True

  print('[rpm'  + str(pin_num + 1) + ']   --- ok')
  if pin_num == 0: q.put(dict(rpm1 = cnt))
  else: q.put(dict(rpm2 = cnt))


def main():
  JST = pytz.timezone('Asia/Tokyo')
  FILE_PATH = str('/home/pi/data/' + str(datetime.now(JST).strftime('%Y/%m/%d')))

  if not (os.path.isdir(FILE_PATH)):
    os.makedirs(FILE_PATH)
  WRITE_PATH = FILE_PATH + '/' + str(datetime.now(JST).strftime('%H:%M:%S')) + '_started'+ '.csv'
  try:
    while True:
      
      start_time = datetime.now(JST)
      threadlist = list()
      threadlist.append(threading.Thread(target=put_water_level()))
      threadlist.append(threading.Thread(target=put_temp()))
      threadlist.append(threading.Thread(target=rpm_get,args=(0,)))
      threadlist.append(threading.Thread(target=rpm_get,args=(1,)))

      for thread in threadlist:
        thread.start()

      for thread in threadlist:
        thread.join()
      
      data = q.get()
      while not q.empty():
        data.update(q.get())
      
      print(data)
      f = open(WRITE_PATH,'a')
      writer = csv.writer(f,lineterminator='\n')

      write_data = list()
      write_data.append(str(datetime.now(JST).strftime('%H:%M:%S')))
      write_data.append(str(data['temp1']))
      write_data.append(str(data['level1']))
      write_data.append(str(data['level2']))
      write_data.append(str(data['rpm1']))
      write_data.append(str(data['rpm2']))
      writer.writerow(write_data)
      f.close()

      stop_time = datetime.now(JST)
      process_time = stop_time - start_time
      print('process time : ' + str(process_time.seconds) + '.'  + str(process_time.microseconds))
      
  except KeyboardInterrupt:
    print('keyboard interrupt!!!')
if __name__ == '__main__':
  main()
