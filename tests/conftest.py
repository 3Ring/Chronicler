import os
import pytest
import pytest_asyncio
import asyncio
from tempfile import TemporaryDirectory
from io import TextIOWrapper
from tests.helpers._async import run_parallel, run_sequence
from tests.helpers.all import make_id
from tests.integration.startup.mockuser import Mock, MockUser

# from tests.fixtures.unit_test.app import *  # noqa
# from tests.fixtures.unit_test.helpers import *
from tests.integration.startup.server import Server
from tests.integration.browser.brands import Browsers


def pytest_addoption(parser):
    parser.addoption("--no-tear-down", action="store")
    parser.addoption("--workers", action="store")


def make_mock(fp: TextIOWrapper):
    _id = make_id(fp=fp)
    return MockUser(_id)


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
# @pytest_asyncio.fixture(scope="session", params=["chrome"])
@pytest_asyncio.fixture(scope="session", params=["chrome", "firefox", "edge"])
async def browsers(request, start_up):
    print(f"brand called")
    print(f"starting tests on {request.param}..")
    brand = Browsers(request.param)
    amount = int(request.config.getoption("--workers"))
    _browsers = await run_parallel(
        *(asyncio.to_thread(brand.get) for _ in range(amount))
    )
    yield _browsers
    await run_parallel(*(asyncio.to_thread(b["driver"].quit) for b in _browsers))


@pytest_asyncio.fixture(scope="module")
async def mocks(fp, browsers):
    print(f"mocks called")
    mocks = [Mock(user=make_mock(fp=fp), browser=b["driver"], brand=b["brand"]) for b in browsers]
    yield mocks
