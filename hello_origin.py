import asyncio


async def main():
    print('hello')
    await asyncio.sleep(1)
    print('world')


# asyncio.run(main())
# 等价于下面的过程

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main())
    loop.run_until_complete(main())
finally:
    loop.close()
