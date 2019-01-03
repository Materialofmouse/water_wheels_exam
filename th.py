import time
import threading

def t(string):
  while True:
    print("hello from " + string)
    time.sleep(1)
  
if __name__ == "__main__":
  thread1 = threading.Thread(target=t,args='a') 
  thread2 = threading.Thread(target=t,args='m')
  thread1.start()
  thread2.start()
  thread1.join()
  thread2.join()
  
  while True:
    time.sleep(0.1)
    
      
