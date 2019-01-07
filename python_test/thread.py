import threading
import time
from datetime import datetime

def t(string,t):
  while True:
    time.sleep(t)
    print(string)

if __name__ == '__main__':
  thread1 = threading.Thread(target=t,args=('a',1))
  thread2 = threading.Thread(target=t,args=('m',2))
  thread1.start()
  thread2.start()
  while True:
    thread1.join()
    thread2.join()

  #while True:
   # time.sleep(2)
