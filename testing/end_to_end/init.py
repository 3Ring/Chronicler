from __future__ import annotations


import os


from selenium import webdriver
from _pytest.fixtures import SubRequest
from selenium.webdriver.support.ui import WebDriverWait

from testing.end_to_end.browser import BrowserUI, BrowserInitializer
from testing.end_to_end import Mock
from testing.end_to_end.models import Users


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


def mock(browser: webdriver) -> Mock:
    ui = BrowserUI(browser)
    user = Users()
    return Mock(ui, user)
