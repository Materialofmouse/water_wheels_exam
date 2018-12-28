import time
import threading

check_flag = False
flag = False

def t():
  while True:
    global flag
    if flag == False:
      check_flag = False
      continue
    
    flag = False
    time.sleep(1)
    check_flag = True
    return check_flag

if __name__ == "__main__":
  thread = threading.Thread(target=t)
  thread.start()

  if check_flag == True:
    print(flag)
    flag = True
    print(1)
    
