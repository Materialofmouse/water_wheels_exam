import Adafruit_ADS1x15 as ads
import time

CHANNEL = 0
GAIN = 2
#16bit 
adc = ads.ADS1115()

while True:
  v = float(adc.read_adc(CHANNEL, gain=GAIN)) * 2.048 / 32768 - 2.464
  level = v / 0.33
  print(str(round(level,1)) + ' cm')
  
  time.sleep(0.5)
