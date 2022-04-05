import os
import pytest
import pytest_asyncio
import asyncio
from tempfile import TemporaryDirectory

# from tests.fixtures.unit_test.app import *  # noqa
# from tests.fixtures.unit_test.helpers import *
from tests.integration.startup.server import Server
from tests.integration.browser.brands import Browsers
from tests.helpers.integration import run_parallel, make_mock


def pytest_addoption(parser):
    parser.addoption("--no-tear-down", action="store")
    parser.addoption("--workers", action="store")


@pytest.fixture(scope="session", autouse=True)
def temp_dir():
    print(f"temp_dir called")
    with TemporaryDirectory() as tdp:
        yield tdp


@pytest.fixture(scope="session", autouse=True)
def fp(temp_dir: TemporaryDirectory):
    print(f"fp called")
    with open(os.path.join(temp_dir, "inc"), "x+") as fp:
        fp.write(str(0))
        yield fp


@pytest_asyncio.fixture(scope="session")
async def start_up(request):
    server = Server(request.config.getoption("--no-tear-down"))
    await server.start_server()
    yield
    print(f"tearing down")
    await server.teardown_server()


@pytest.fixture(scope="session")
def event_loop():
    """A session-scoped event loop."""
    loop = asyncio.SelectorEventLoop()
    yield loop
    loop.close()


# @pytest_asyncio.fixture(scope="module", params=["chrome", "chrome", "chrome"])
# @pytest_asyncio.fixture(scope="module", params=["chrome", "firefox", "edge"])
@pytest_asyncio.fixture(scope="session", params=["chrome"])
async def browsers(request, start_up):
    print(f"brand called")
    print(f"starting tests on {request.param}..")
    brand = Browsers(request.param)
    amount = 3
    _browsers = await run_parallel(*(brand.get() for _ in range(amount)))
    yield _browsers
    await run_parallel(*(asyncio.to_thread(b["driver"].close) for b in _browsers))


@pytest_asyncio.fixture(scope="function")
async def mocks(fp, browsers, request):
    print(f'mocks called')
    mocks = [
        make_mock(fp=fp, browser=b["driver"], brand=b["brand"])
        for _, b in zip(range(request.param), browsers)
    ]
    yield mocks
    await run_parallel(*(m.reset()for m in mocks))
        
