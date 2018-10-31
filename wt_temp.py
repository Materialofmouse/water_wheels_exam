#water temp input test
import subprocess
import time

temp_dir = ['cat','/sys/class/hwmon/hwmon0/temp1_input']
res = subprocess.check_output(temp_dir)
print(int(res))
