import threading
import queue
import RPi.GPIO as GPIO
import time
import sys
from datetime import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

level_pin = [[15,18,23,24],[12,16,20,21]]
rpm_pin = [17,27]

GPIO.setup(level_pin[0], GPIO.IN)
GPIO.setup(level_pin[1], GPIO.IN)
GPIO.setup(rpm_pin,GPIO.IN)

q = queue.Queue()

def set_water_level():
  print('[level]  --- start')
  level = [0] * 2
  
  for i,pin_num in enumerate(level_pin):
    for pin in pin_num:
      level[i] += not GPIO.input(pin)
   
  q.put(dict(level1=level[0] + 1, level2=level[1] + 1))
  print('[level]  --- ok')


def set_water_temp():
  import subprocess
  #--- get water level ---
  print('[temp]   --- start')
  t = int(subprocess.check_output(['cat','/sys/class/hwmon/hwmon0/temp1_input']))
  t = t / 1000
  q.put(dict(temp = t))
  print('[temp]   --- ok')


def rpm_get(pin_num):
  start_time = datetime.now()
  cnt = 0
  flag = True
  print('[rpm' + str(pin_num + 1) +']   --- start')
  
  while not (datetime.now() - start_time).seconds == 10:
    if GPIO.input(rpm_pin[pin_num]) == True and flag == True:
      flag = False
      cnt += 1
    elif GPIO.input(rpm_pin[pin_num]) == False:
      flag = True

  print('[rpm'  + str(pin_num + 1) + ']   --- ok')
  if pin_num == 0: q.put(dict(rpm1 = cnt))
  else: q.put(dict(rpm2 = cnt))


def main():
  import os
  import pytz
  import csv


  JST = pytz.timezone('Asia/Tokyo')
  file_path = str('/home/pi/data/' + str(datetime.now(JST).strftime('%Y/%m/%d')))

  if not (os.path.isdir(file_path)):
    os.makedirs(file_path)
  write_path = file_path + '/' + str(datetime.now(JST).strftime('%H:%M:%S')) + '_started'+ '.csv'
  try:
    while True:
      
      start_time = datetime.now(JST)
      threadlist = list()
      threadlist.append(threading.Thread(target=set_water_level()))
      threadlist.append(threading.Thread(target=set_water_temp()))
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
      f = open(write_path,'a')
      writer = csv.writer(f,lineterminator='\n')

      write_data = list()
      write_data.append(str(datetime.now(JST).strftime('%H:%M:%S')))
      write_data.append(str(data['temp']))
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
