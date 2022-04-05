from typing import Any, Awaitable

import asyncio
from asyncio import SelectorEventLoop
from tests.integration.startup.mockuser import Mock, MockUser
from io import TextIOWrapper
from tests.integration.browser.brands import Browsers
from tests.helpers.all import get_and_increment, make_id

async def run_sequence(*functions: Awaitable[Any]) -> Any:
    for function in functions:
        rets = await function
    return rets


async def run_parallel(*functions: Awaitable[Any]) -> Any:
    return await asyncio.gather(*functions)


def make_mock(
    fp: TextIOWrapper, browser: Browsers, brand: str
):
    _id = make_id(fp=fp)
    user = MockUser(_id)
    return Mock(user=user, brand=brand, browser=browser)
