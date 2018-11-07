import Adafruit_ADS1x15 as ads
import time

CHANNEL = 0
GAIN = 2
#16bit 
adc = ads.ADS1115()

while True:
  v = float(adc.read_adc(CHANNEL, gain=GAIN)) * 2.048 / 32768
  level = 21.03 - (((v / 21.4) * 1000 - 26.4) / 2.35)
  print(str(round(level,2)) + ' cm')
  
  time.sleep(0.5)
