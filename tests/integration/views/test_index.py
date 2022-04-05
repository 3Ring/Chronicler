import pytest
from tests.helpers.integration import run_parallel, run_sequence
from tests.integration.startup.mockuser import Mock


@pytest.mark.asyncio
@pytest.mark.parametrize("mocks", [1], indirect=True)
async def test_one(mocks: list[Mock]):
    print(f"1")
    print(f'mock: {mocks}')


async def populate(user: Mock) -> Mock:
    await user.register()
    return user

@pytest.mark.parametrize("mocks", [3], indirect=True)
@pytest.mark.asyncio
async def test_two(mocks: list[Mock]):
    print(f'mocks: {mocks}')
    populated = await run_parallel(*(populate(m) for m in mocks))
    print(f"2")
    print(f"start_up: {populated}")
    [print(f'populated.current_url: {p.browser.current_url}') for p in populated]
