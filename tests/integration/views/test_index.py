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


@pytest.mark.asyncio
async def test_index(mocks: list[Mock], fp: TextIOWrapper):
    test_queue = asyncio.Queue()
    browser_queue = asyncio.Queue()
    for mock in mocks:
        await browser_queue.put(mock)
    for task in [
        page_assets,
        # my_dm_games_are_visible,
        # my_pc_games_exist,
        # user_must_be_logged_in,
    ]:
        await test_queue.put(task)
    await run_parallel(
        *(
            asyncio.create_task(worker(test_queue, browser_queue, fp))
            for _ in range(len(mocks))
        )
    )


async def page_assets(mock: Mock):
    print("page_assets")
    await run_sequence(
        mock.register(),
        mock.login(),
    )
    await run_parallel(
        mock.get_element((By.XPATH, "//a[@href='/create/game']")),
        mock.get_element((By.XPATH, "//a[@href='/join']")),
        mock.auth_nav(),
    )


async def my_dm_games_are_visible(mock: Mock):
    print("TODO: my_dm_games_are_visible")


async def my_pc_games_exist(mock: Mock):
    print("TODO: my_pc_games_exist")


async def user_must_be_logged_in(mock: Mock):
    print("user_must_be_logged_in")
    await mock.nav(url=chron_url("/index"), next=chron_url("/", next="/index"))


async def populate(user: Mock) -> Mock:
    from tests.conftest import fp
    game = generate_game(fp)
    await user.register()
    await user.login()
    await user.create_game(game)
    return game
