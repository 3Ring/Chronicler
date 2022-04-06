import asyncio
from tests.integration.startup.mockuser import Mock
from io import TextIOWrapper


async def worker(tests: asyncio.Queue, mocks: asyncio.Queue[Mock], fp: TextIOWrapper):
    """
    Takes a test function and a mocked User/browser from their respective queues and runs them together.

    :param tests: asyncio.Queue filled with test functions
    :param mocks: asyncio.Queue[Mock] filled with mock Users/Browsers
    :param fp: The file pointer to the file that contains the incrementing id used to create unique users
    """
    while not tests.empty():
        if mocks.empty():
            await asyncio.sleep(.1)
            continue
        test = await tests.get()
        mock = await mocks.get()
        await test(mock)
        mock.reset(fp)
        await mocks.put(mock)
