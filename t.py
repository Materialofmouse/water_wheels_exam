import threading
import queue
import RPi.GPIO as GPIO
import datetime
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

level_pin = [[15,18,23,24],[12,16,20,21]]
GPIO.setup(level_pin[0], GPIO.IN)
GPIO.setup(level_pin[1], GPIO.IN)

q = queue.Queue()

def set_water_level():
  global level_pin
  level = [0] * 2

  for i,pin_num in enumerate(level_pin):
    for pin in pin_num:
      level[i] += not GPIO.input(pin)
   
  global q
  q.put(dict(level1=level[0], level2=level[1]))
  print('[level] --- ok')

def set_water_temp():
  #--- get water level ---
  global q
  q.put(dict(temp = 20.5))
  print('[temp] --- ok')

def on_timer():
  time.sleep(10)
  print('10s') 

def main():
  while True:
    threadlist = list()
    threadlist.append(threading.Thread(target=set_water_level()))
    threadlist.append(threading.Thread(target=set_water_temp()))
    threadlist.append(threading.Thread(target=on_timer()))
    
    for thread in threadlist:
      thread.start()

    for thread in threadlist:
      thread.join()
    
    data = q.get()
    while not q.empty():
      data.update(q.get())
      

    print(data)

  ## --- kaki komi syori ---

if __name__ == '__main__':
  main()
