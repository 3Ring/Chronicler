import asyncio
from typing import Any, Awaitable


async def run_sequence(*functions: Awaitable[Any]) -> Any:
    for function in functions:
        rets = await function
    return rets


async def run_parallel(*functions: Awaitable[Any]) -> Any:
    return await asyncio.gather(*functions)
