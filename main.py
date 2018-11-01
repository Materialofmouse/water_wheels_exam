#software
import os
import csv
from datetime import datetime
import threading

#hardware
import Adafruit_ADS1x15
import RPi.GPIO as gpio
import subprocess

gpio.setmode(gpio.BCM)
gpio.setup(16,gpio.OUT)#down pomp
gpio.setup(20,gpio.OUT)#up pomp

#high 
gpio.output(16,True)
gpio.output(20,True)

def get_temp():
  temp = 10
  return temp

#water tempracture return int
def get_wt_temp():
  return float(subprocess.check_output(['cat','/sys/class/hwmon/hwmon0/temp1_input'])) / 100

#cpu tempracture return int
def get_cpu_temp():
  temp = 50
  return temp

#get water level,return int(0.5cm)
def get_wt_level():
  volt = Adafruit_ADS1x15.ADS1115().read_adc(0,gain=2)
  level = volt * 2.048 / 32768
  return level #

#update later
def control_water_level(level):
  #gpio.setup(16,gpio.OUT)
    
  sec = 0.2
  level_now = get_wt_level()
  while level_now == level:
    
    #up control
    if level_now > level:
      gpio.output(16,False)

    #donw control
    else:
      gpio.output(20,False)

    time.sleep(sec)
    
    #update now water level
    gpio.output(16,True)
    gpio.output(20,True)
    level_now = get_wt_level()
  
  gpio.cleanup()
  return level_now

#input the value that will change the water level
def input_water_level():
  
  print("input the watar level")
  level = input()
  while type(level) is not int:
    level = input()
  
  return control_water_level(watar_level)

#output data path
path = str(os.getcwd()) + '/data/' + str(datetime.now().strftime('%Y/%m/%d'))


if __name__ == '__main__':

  #make dir from date
  if not (os.path.isdir(path)):
    os.makedirs(path)
  
  try:
    print('running program') 
    thread = threading.Thread(target=input_water_level)
    thread.start()

    while True:
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

  except KeyboardInterrupt:
    gpio.cleanup()
    exit()
