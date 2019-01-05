import asyncio
import time
import datetime

async def test():
  await asyncio.sleep(1)
  return datetime.datetime.now()

async def func():
  await asyncio.sleep(1)
  return "aaa"

async def main():
  a = 1
  b = 2
  while True:
    print(datetime.datetime.now())
    b = await test() 
    res  = await func()
    print(b)
    print(res)

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.close()
