import pytest
from tests.helpers.all import (
    chron_url,
    generate_game,
)
from tests.helpers._async import run_parallel, run_sequence
from tests.helpers.worker import worker
from tests.integration.startup.mockuser import Mock
from io import TextIOWrapper
import asyncio
from selenium.webdriver.common.by import By
# Games

@pytest.mark.asyncio
async def test_index(mocks: list[Mock], fp: TextIOWrapper):
    test_queue = asyncio.Queue()
    browser_queue = asyncio.Queue()
    for mock in mocks:
        await browser_queue.put(mock)
    for task in [
        bad_game_names,
        bad_game_images,
        game_can_be_published,
        user_can_create_game,
        game_has_assets,
        user_can_create_dm,
        bad_dm_names,
        bad_dm_images,
        bad_character_names,
        bad_character_images,
        bad_character_bios,
        user_can_create_character,
    ]:
        await test_queue.put(task)
    await run_parallel(
        *(
            asyncio.create_task(worker(test_queue, browser_queue, fp))
            for _ in range(len(mocks))
        )
    )

async def bad_game_names(mock: Mock):
    print('TODO: bad_game_names')

async def bad_game_images(mock: Mock):
    print('TODO: bad_game_images')

async def game_can_be_published(mock: Mock):
    print('TODO: game_can_be_published')

async def user_can_create_game(mock: Mock):
    print('TODO: user_can_create_game')

async def game_has_assets(mock: Mock):  
    print('TODO: game_has_assets')



# DM
async def user_can_create_dm(mock: Mock):
    print('TODO: user_can_create_dm')

async def bad_dm_names(mock: Mock):
    print('TODO: bad_dm_names')

async def bad_dm_images(mock: Mock):
    print('TODO: bad_dm_images')


# Character
async def bad_character_names(mock: Mock):
    print('TODO: bad_character_names')

async def bad_character_images(mock: Mock):
    print('TODO: bad_character_images')

async def bad_character_bios(mock: Mock):
    print('TODO: bad_character_bios')

async def user_can_create_character(mock: Mock):
    print('TODO: user_can_create_character')




