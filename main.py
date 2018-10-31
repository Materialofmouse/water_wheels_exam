#software
import os
import csv
from datetime import datetime

#hardware
import Adafruit_ADS1x15
import RPi.GPIO as gpio
import subprocess


def get_temp():
  temp = 10
  return temp

  #water tempracture
def get_wt_temp():
  return float(subprocess.check_output(['cat','/sys/class/hwmon/hwmon0/temp1_input'])) / 100

  #cpu tempracture
def get_cpu_temp():
  temp = 50
  return temp

def get_wt_level():
  return Adafruit_ADS1x15.ADS1115().read_adc(2,gain=1)

def control_water_level():
  return 10



  #outside tempracture
  
#output data path
path = str(os.getcwd()) + '/data/' + str(datetime.now().strftime('%Y/%m/%d'))


if __name__ == '__main__':

  #make dir from date
  if not (os.path.isdir(path)):
    os.makedirs(path)
  
  
  #make file from date 
  f = open(path + '/' + str(datetime.now().strftime('%H:%M:%S')) + '.csv','w')
  writer = csv.writer(f,lineterminator='\n')
  
  data = []
  data.append(str(datetime.now().strftime('%H:%M:%S')))
  data.append(str(get_temp()))
  data.append(str(get_wt_temp()))
  data.append(str(get_cpu_temp()))
  data.append(str(get_wt_level()))
  
  #write data to csv file
  writer.writerow(data)

  f.close()
