import os


from selenium import webdriver
from _pytest.fixtures import SubRequest
from selenium.webdriver.support.ui import WebDriverWait

from end_to_end.browser.ui import BrowserUI
from end_to_end.browser.browsers import BrowserInitializer
from end_to_end.browser.actions.check_actions import CheckActions
from end_to_end.browser.actions.create_actions import CreateActions
from end_to_end.browser.actions.auth_actions import AuthActions
from end_to_end.browser.actions.edit_actions import EditActions
from end_to_end.browser.actions.story_actions import StoryActions
from end_to_end.mock import Mock
from end_to_end.assets import User
from _logging import Logger


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
    user = User()
    check = CheckActions(ui, logger)
    auth = AuthActions(ui, logger, user, check)
    create = CreateActions(ui, logger, user, check)
    edit = EditActions(ui, logger, user, check)
    actions = StoryActions(ui, logger, user, check, auth, create)
    return Mock(ui, logger, user, actions, check, auth, create, edit)
