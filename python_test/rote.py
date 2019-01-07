import RPi.GPIO as GPIO
import time
import threading
import queue

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

GPIO.setup(17,GPIO.IN)

timeflag = False


q = queue.Queue()

def on_timer():
  global timeflag
  print('time',end='')
  print(timeflag)
  time.sleep(5)
  timeflag = True


def counter():
  
  print('cnt',end='')
  print(timeflag)
  flag = True
  cnt = 0
  
  while not timeflag:
    print('a')
    if GPIO.input(17) == True and flag == True:
      flag = False
      cnt += 1
      print(cnt)
    elif GPIO.input(17) == False:
      flag = True
  
  print(cnt)


if __name__ == '__main__':
  t = 5
  timer = threading.Thread(target=on_timer())
  count = threading.Thread(target=counter())
  print(timeflag)
  
  count.start()
  timer.start()

  count.join()  
  timer.join()
