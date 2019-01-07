import Adafruit_ADS1x15 as ads
import time

CHANNEL = 3
GAIN = 2
#16bit 
adc = ads.ADS1115()

while True:
  v = float(adc.read_adc(CHANNEL, gain=GAIN)) * 2.048 / 32768
  #level = (20.85 - (((v - 0.56) * 1000 / 21.4) * 0.42) )
  level = v
  print(level)
  
  time.sleep(0.5)
