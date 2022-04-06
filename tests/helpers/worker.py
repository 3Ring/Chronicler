import asyncio
from tests.integration.startup.mockuser import Mock
from io import TextIOWrapper


async def worker(tests: asyncio.Queue, mocks: asyncio.Queue[Mock], fp: TextIOWrapper):
    while not tests.empty():
        if mocks.empty():
            await asyncio.sleep(1)
            continue
        test = await tests.get()
        mock = await mocks.get()
        await test(mock)
        mock.reset(fp)
        await mocks.put(mock)
