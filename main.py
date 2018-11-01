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

gpio.setmode(gpio.BCM)
gpio.setup(16,gpio.OUT)#down pomp
gpio.setup(20,gpio.OUT)#up pomp

#high 
gpio.output(16,True)
gpio.output(20,True)

class control_water_level(threading.Thread):
  def __init__(self):
    super(control_water_level,self).__init__()

  

def get_temp():
  temp = 10
  return temp

#water tempracture return int
def get_water_temp():
  return float(subprocess.check_output(['cat','/sys/class/hwmon/hwmon0/temp1_input'])) / 100

#cpu tempracture return int
def get_cpu_temp():
  temp = 50
  return temp

#get water level,return int(0.5cm)
def get_water_level():
  volt = Adafruit_ADS1x15.ADS1115().read_adc(0,gain=2)
  level = volt * 2.048 / 32768
  return level #

def test_water_level():
  return 10

#update later
def control_water_level(level):
  #gpio.setup(16,gpio.OUT)
    
  sec = 0.5
  level_now = get_water_level()
  
  while not level_now == level:
    
    #up control
    if level_now > level:
      gpio.output(16,False)
      print('now level is ' + str(level_now) + ',up now...,' )

    #donw control
    else:
      gpio.output(20,False)
      print('now level is ' + str(level_now) +',down now')

    time.sleep(sec)
    
    #update now water level
    level_now = get_water_level()

  gpio.output(16,True)
  gpio.output(20,True)
 
  gpio.cleanup()
  return level_now

def test_control(level):
  
  for i in range(level):
    time.sleep(0.5)
    gpio.output(16,False)

#input the value that will change the water level
def input_water_level():
  
  while True:
    
    level = input('plase input water level:')
    try:
      level = int(level)
      return control_water_level(level)

    except ValueError:
      print('plase input intager value!!!!!!')
      continue

  return False

#output data path
path = str(os.getcwd()) + '/data/' + str(datetime.now().strftime('%Y/%m/%d'))


if __name__ == '__main__':

  #make dir from date
  if not (os.path.isdir(path)):
    os.makedirs(path)
  
  thread = threading.Thread(target=input_water_level)
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
      data.append(str(get_temp()))
      data.append(str(get_water_temp()))
      data.append(str(get_cpu_temp()))
      data.append(str(get_water_level()))
      
      #write data to csv file
      writer.writerow(data)

      f.close()

  except KeyboardInterrupt:
    gpio.cleanup()
    exit()
