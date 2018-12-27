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

def get_temp():
  temp = 10
  return temp

#water tempracture return int
def get_water_temp():
  return float(subprocess.check_output(['cat','/sys/class/hwmon/hwmon0/temp1_input'])) / 1000

#get water level,return int(0.5cm)
def get_water_level():
  volt = Adafruit_ADS1x15.ADS1115().read_adc(1,gain=2)
  level = volt * 2.048 / 32768
  level = 20.85 - (((level - 0.56) * 1000 / 21.4) * 0.42 )
  return round(level,0)


JST = pytz.timezone('Asia/Tokyo')
#make dir from now time
path = str( '/home/pi/data/' + str(datetime.now(JST).strftime('%Y/%m/%d')))
if not (os.path.isdir(path)):
  os.makedirs(path)
path = path + '/' + str(datetime.now(JST).strftime('%H:%M:%S')) + '.csv'

gpio.setmode(gpio.BCM)
gpio.setup(21,gpio.OUT)
gpio.output(21,True)

while True:
  #make file from date 
  f = open(path,'a')
  writer = csv.writer(f,lineterminator='\n')
  #make write data
  data = []
  data.append(str(datetime.now(JST).strftime('%H:%M:%S')))
  data.append(str(get_temp()))
  data.append(str(get_water_temp()))
  data.append(str(get_water_level()))
  
  #write data to csv file
  writer.writerow(data)
  f.close()
  gpio.output(21,False)
  time.sleep(0.05)
  gpio.output(21,True)
  time.sleep(0.95)
