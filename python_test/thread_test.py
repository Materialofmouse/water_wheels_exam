import threading
import time
from datetime import datetime

def func():
  print('hello from func')
  print('hello from func')


def test():
  print('hello from test')
  print('hello from test')


if __name__ == '__main__':
  thread1 = threading.Thread(target=func())
  thread2 = threading.Thread(target=test())

  thread2.start()
  thread1.start()

  thread2.join()
  thread1.join()

  
