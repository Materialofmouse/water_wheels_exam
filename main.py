#software
import os
import csv
from datetime import datetime
import threading
import pytz
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

  #get water level,return int(0.5cm)
  def get_water_level(self):
    volt = Adafruit_ADS1x15.ADS1115().read_adc(0,gain=2)
    level = volt * 2.048 / 32768
    level = 20.85 - (((level - 0.56) * 1000 / 21.4) * 0.42 )
    return round(level,0)


class data_write(threading.Thread,sensors):
  def __init__(self):
    self.JST = pytz.timezone('Asia/Tokyo')
    #make dir from now time
    self.path = str(os.getcwd()) + '/data/' + str(datetime.now(self.JST).strftime('%Y/%m/%d'))
    if not (os.path.isdir(self.path)):
      os.makedirs(self.path)
    self.path = self.path + '/' + str(datetime.now(self.JST).strftime('%H:%M:%S')) + '.csv'
    super().__init__()
  
  def run(self):
    while True:
      #make file from date 
      f = open(self.path,'a')
      writer = csv.writer(f,lineterminator='\n')
      #make write data
      data = []
      data.append(str(datetime.now(self.JST).strftime('%H:%M:%S')))
      data.append(str(sensors().get_temp()))
      data.append(str(sensors().get_water_temp()))
      data.append(str(sensors().get_water_level()))
      
      #write data to csv file
      writer.writerow(data)
      f.close()
      time.sleep(1)
    
    return True


if __name__ == '__main__':

  gpio.setmode(gpio.BCM)
  gpio.setup(16,gpio.OUT)
  gpio.setup(20,gpio.OUT)
  gpio.output(16,False)
  gpio.output(20,False)

  thread = data_write()
  thread.start()
  print('program started') 

  #input water level
  try:  
    while True:     
      level = input('plase input water level:')
      try:
        level = int(level)

      except ValueError:
        print('plase input intager value!!!!!!')
        continue

      time.sleep(1)

      sec = 1
      level_now = sensors().get_water_level() 
      while not level_now == level:
        #up control
        if level_now > level:
          gpio.output(16,True)
          print('now level is ' + str(level_now) + ',down now...' )
        #down control
        else:
          gpio.output(20,True)
          print('now level is ' + str(level_now) +',up now')

        time.sleep(sec)
        level_now = sensors().get_water_level()

        gpio.output(16,False)
        gpio.output(20,False)
      
      gpio.cleanup()
      
  except KeyboardInterrupt:
    gpio.cleanup()
    exit()
