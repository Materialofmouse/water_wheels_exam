import signal
import time

def test(arg,arg1):
  print(time.time())

signal.signal(signal.SIGALRM, test)
signal.setitimer(signal.ITIMER_REAL,1,1)

while True:
  time.sleep(1)
