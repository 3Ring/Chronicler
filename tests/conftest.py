import inspect
import pytest
import tempfile

from tests.fixtures.unit_test.app import *  # noqa
from tests.fixtures.unit_test.helpers import *  # noqa
from tests.fixtures.integration.server import *  # noqa
from tests.fixtures.integration.browser import *  # noqa


# def pytest_collection_modifyitems(config, items):
#     for item in items:
#         if inspect.iscoroutinefunction(item.function):
#             item.add_marker(pytest.mark.asyncio)

import asyncio
import pytest_asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

thread_local = threading.local()
def pytest_addoption(parser):
    parser.addoption("--no-tear-down", action="store")
    parser.addoption("--workers", action="store")

@pytest.fixture(scope="session")
def temp_dir():
    print(f'temp_dir called')
    with tempfile.TemporaryDirectory() as tdp:
        yield tdp


@pytest.fixture(scope="session")
def inc(temp_dir):
    print(f'inc called')
    with open(os.path.join(temp_dir, "inc"), "x+") as fp:
        fp.write(str(0))
        yield fp

@pytest.fixture(scope="session", params=["chrome"])
# @pytest.fixture(scope="session", params=["chrome", "firefox", "edge"])
def brand(server, request):
    print(f'brand called')
    print(f'starting tests on {request.param}..')
    yield request.param



@pytest.fixture(scope="session")
def threads(request):
    print(f'threads called')
    amount = int(request.config.getoption("--workers"))
    print(f'amount: {amount}')
    with ThreadPoolExecutor(max_workers=amount) as executor:
        yield executor
# @pytest.fixture(scope="module")
# def event_loop():
#     """A module-scoped event loop."""
#     return asyncio.new_event_loop()