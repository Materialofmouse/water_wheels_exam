import csv
from datetime import datetime
import os
#import Adafruit_ADS1x15 as ads
#import RPi.GPIO as gpio

#outside tempracture
def get_temp():
  temp = 10
  return temp

#water tempracture
def get_wt_temp():
  temp = 20
  return temp

#cpu tempracture
def get_cpu_temp():
  temp = 50
  return temp

def get_wt_level():
  level = 22
  return level

def control_water_level(level):
  return

path = str(os.getcwd()) + '/data/' + str(datetime.now().strftime('%Y/%m/%d'))


if __name__ == '__main__':

  #make dir from date
  if not (os.path.isdir(path)):
    os.makedirs(path)
  
  #make file from date 
  f = open(path + '/' + str(datetime.now().strftime('%H:%M:%S')) + '.csv','w')
  

  data = []
  data.append(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
  data.append(str(get_temp()))
  data.append(str(get_wt_temp()))
  data.append(str(get_cpu_temp()))
  data.append(str(get_wt_level()))
  
  #write data to csv file
  writer = csv.writer(f,lineterminator='\n')
  writer.writerow(data)

  f.close()
