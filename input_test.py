import threading
import time
import os

def test():

  while True:
    a = input('plase input')
    try:
      int(a)
      return print(a)

    except ValueError:
      print('please input intager value!!')

  return False

t = threading.Thread(target=test)
t.start()

while True:
  time.sleep(1)
