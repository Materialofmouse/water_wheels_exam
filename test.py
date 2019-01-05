import asyncio
import sys
import time
sys.path.append('/usr/local/lib/python3.5/dist-packages')
import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
level_pin = [[15,18,23,24],[12,16,20,21]]
GPIO.setup(level_pin, GPIO.IN)

async def get_water_level():
  await asyncio.sleep(1)

async def get_temp():
  await asyncio.sleep(1)
  #--- atodekaku ---
  return 20.5

async def main():
  while True:
    task1 = asyncio.create_task(get_watar_level())
    task2 = asyncio.create_task(get_temp())

    level = await task1 
    res  = await task2
    print(b)
    print(res)

asyncio.run(main())
