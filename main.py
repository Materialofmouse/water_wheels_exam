#software
import os
import csv
from datetime import datetime
import threading
#hardware
import Adafruit_ADS1x15
import RPi.GPIO as gpio
import subprocess
import time


class sensors():
  def __init__(self):
    pass

  def get_temp(self):
    temp = 10
    return temp

  #water tempracture return int
  def get_water_temp(self):
    return float(subprocess.check_output(['cat','/sys/class/hwmon/hwmon0/temp1_input'])) / 100

  #cpu tempracture return int
  def get_cpu_temp(self):
    temp = 50
    return temp

  #get water level,return int(0.5cm)
  def get_water_level(self):
    volt = Adafruit_ADS1x15.ADS1115().read_adc(0,gain=2)
    level = volt * 2.048 / 32768
    return level

  def test_water_level():
    return 10


class control(threading.Thread,sensors):
  def __init__(self):
    super(control,self).__init__()
    #gpio settings,16:up,20:down
    gpio.setmode(gpio.BCM)
    gpio.setup(16,gpio.OUT)
    gpio.setup(20,gpio.OUT)
    #always high 
    gpio.output(16,True)
    gpio.output(20,True)

  def run(self):
    while True:     
      level = input('plase input water level:')
      try:
        level = int(level)
        control.control_water_level(self,level)

      except ValueError:
        print('plase input intager value!!!!!!')
        continue

    return False

  def control_water_level(self,level):
    #gpio.setup(16,gpio.OUT)
    sec = 0.5
    level_now = sensors().get_water_level()
    
    gpio.setmode(gpio.BCM)
    gpio.setup(16,gpio.OUT)
    gpio.setup(20,gpio.OUT)
    
    while not level_now == level:
      #up control
      if level_now > level:
        gpio.output(16,False)
        print('now level is ' + str(level_now) + ',up now...' )
      #down control
      else:
        gpio.output(20,False)
        print('now level is ' + str(level_now) +',down now')

      time.sleep(sec)
      level_now = sensors().get_water_level()

    gpio.output(16,True)
    gpio.output(20,True)
    gpio.cleanup()
    return level_now


if __name__ == '__main__':
  #make dir from date
  path = str(os.getcwd()) + '/data/' + str(datetime.now().strftime('%Y/%m/%d'))
  if not (os.path.isdir(path)):
    os.makedirs(path)
  
  thread = control()
  sensor = sensors()
  thread.start()
  print('running program') 
  
  try:  
    path = path + '/' + str(datetime.now().strftime('%H:%M:%S')) + '.csv'
    while True:
      #make file from date 
      f = open(path,'w')
      writer = csv.writer(f,lineterminator='\n')
      #make write data
      data = []
      data.append(str(datetime.now().strftime('%H:%M:%S')))
      data.append(str(sensor.get_temp()))
      data.append(str(sensor.get_water_temp()))
      data.append(str(sensor.get_cpu_temp()))
      data.append(str(sensor.get_water_level()))
      
      #write data to csv file
      writer.writerow(data)
      f.close()
      time.sleep(5)

  except KeyboardInterrupt:
    gpio.cleanup()
    exit()
