import asyncio


async def main():
    print('hello')
    await asyncio.sleep(1)
    print('world')
    return 1111


# asyncio的入口
asyncio.run(main())
