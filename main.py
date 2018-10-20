import csv
#import Adafruit_ADS1x15 as ads
#import RPi.GPIO as gpio

#outside tempracture
def get_temp():
  return temp

#water tempracture
def get_wt_temp():
  return temp

#cpu tempracture
def get_cpu_temp():
  return temp


def control_water_level(level):
  

f = open('test.csv','w')

writer = csv.writer(f,linterminator='\n')
writer.writerow(data)

f.close()
