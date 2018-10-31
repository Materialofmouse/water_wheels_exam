import Adafruit_ADS1x15 as ads
import time

CHANNEL = 0
GAIN = 2/3
I = 0.0016
adc = ads.ADS1115()

while True:
  v = float(adc.read_adc(CHANNEL, gain=GAIN)) * 6.144 / 32768
  level = (1500 - (v / 0.0016)) / 56
  print(str(level) + ' cm')
  time.sleep(0.5)
