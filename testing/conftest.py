import os
import json
import time
from tempfile import TemporaryDirectory

import pytest
from _pytest.fixtures import SubRequest
from pytest import Parser, Metafunc

from end_to_end import init
from env import ADDOPT_HELP, _load_env
from end_to_end.mock import Mock
from end_to_end import server as _server
from _logging import Logger

_load_env()

def pytest_addoption(parser: Parser):
    parser.addoption(
        "--timeout", default="1.0", action="store", help=ADDOPT_HELP["--timeout"]
    )
    parser.addoption(
        "--fail_timeout",
        default="0.2",
        action="store",
        help=ADDOPT_HELP["--fail_timeout"],
    )
    parser.addoption(
        "--poll_frequency",
        default="0.2",
        action="store",
        help=ADDOPT_HELP["--poll_frequency"],
    )
    parser.addoption(
        "--browser_types",
        default="all",
        action="store",
        help=ADDOPT_HELP["--browser_types"],
    )
    parser.addoption(
        "--log", default="WARNING", action="store", help=ADDOPT_HELP["--log"]
    )


def browser_params(arg_list: str) -> list:
    supported = json.loads(os.environ.get("SUPPORTED_BROWSER_TYPES"))
    browser_types = arg_list.split()
    if browser_types == ["all"]:
        return supported
    for arg in browser_types:
        if arg not in supported:
            raise NotImplementedError()
    return [arg_list]


def pytest_generate_tests(metafunc: Metafunc):
    os.environ.update({"LOG_LEVEL": metafunc.config.getoption("--log")})
    # TODO fix this so that it's not reinstalling the browser every test
    # if "mock" in metafunc.fixturenames:
    #     params = browser_params(metafunc.config.getoption("--browser_types"))
    #     metafunc.parametrize("mock", params, indirect=True, scope="session")


@pytest.fixture(scope="session")
def logger():
    start = time.time()
    with TemporaryDirectory() as tmp:
        logger_ = Logger(tmp)
        try:
            yield logger_
        finally:
            finish = time.time()
            logger_.info(f"tests took {finish - start} seconds")
            for handler in logger_.file.handlers:
                handler.close()
            for handler in logger_.console.handlers:
                handler.close()
            logger_.commit(tmp)



@pytest.fixture(scope="session", autouse=True)
def server(logger: Logger):
    try:
        _server.start_up()
    except Exception:
        logger.error("server exception", exc_info=True)
        raise
    else:
        yield
    finally:
        _server.tear_down()

@pytest.fixture(scope="session", params=browser_params("chrome"))
def mock(request: SubRequest, logger: Logger):
    try:
        browser = init.create_browser(request, logger.level)
        mock_: Mock = init.mock(browser, logger)
    except Exception:
        logger.error("unable to init mocks", exc_info=True)
        raise
    try:
        yield mock_
    finally:
        mock_.ui.browser.quit()

