import Adafruit_ADS1x15 as ads
import time

adc = ads.ADS1115()
volts = adc.startContinuousConversion(0,gain.sps)
start_time = time.time()
i = 0
while i < 1000:
  volts = adc.getLastConversionResults()
  print(volts)
  time(1)
  i += 1
adc.stopContinuousConversion()
