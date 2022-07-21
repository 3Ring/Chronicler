from __future__ import annotations


import os


from selenium import webdriver
from _pytest.fixtures import SubRequest
from selenium.webdriver.support.ui import WebDriverWait

from testing.end_to_end.browser.ui import BrowserUI
from testing.end_to_end.browser.browsers import BrowserInitializer
from testing.end_to_end.browser.checks import CheckActions
from testing.end_to_end.mock import Mock
from testing.end_to_end.models.users import Users
from testing.logger import Logger


def create_browser(request: SubRequest, log_level: int):
    if request.param not in os.environ.get("SUPPORTED_BROWSER_TYPES"):
        raise NotImplementedError()
    poll_frequency = float(request.config.getoption("--poll_frequency"))
    timeout = float(request.config.getoption("--timeout"))
    timeout_when_expecting_fail = float(request.config.getoption("--fail_timeout"))

    wait = WebDriverWait(driver=None, timeout=timeout, poll_frequency=poll_frequency)
    fail_wait = WebDriverWait(
        driver=None, timeout=timeout_when_expecting_fail, poll_frequency=poll_frequency
    )
    launcher = getattr(BrowserInitializer, request.param)

    return launcher(wait, fail_wait, log_level)


def mock(browser: webdriver, logger: Logger) -> Mock:
    ui = BrowserUI(browser, logger)
    user = Users()
    check = CheckActions(ui, logger)
    return Mock(ui, user, check)
