from typing import Tuple
from contextlib import contextmanager

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import (
    presence_of_all_elements_located,
    presence_of_element_located,
    element_to_be_clickable,
)
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
)
from end_to_end.helpers import url_convert
from end_to_end.browser.browsers import TestsBrowser

from _logging import Logger
import env


class BrowserUI:
    def __init__(self, browser: TestsBrowser, logger: Logger) -> None:
        self.browser = browser
        self.logger = logger

    def _click_error_retries(self, element: WebElement, ex: Exception):
        self.logger.info(
            f"{ex.__class__}: {ex.msg}\nAttempting fix by adjusting position"
        )
        if self._adjust_position(element):
            return True
        self.logger.info("Attempting fix by adjusting size")
        return self._adjust_size(element)

    def _adjust_position(self, element: WebElement) -> bool:
        for i in range(20, 100, 20):
            self.logger.debug(f"adjusting page position by {-i}")
            self.browser.set_window_position(0, -i)
            try:
                element.click()
                self.logger.info(f"click successful by adjusting position by {-i}")
                return True
            except (ElementClickInterceptedException, ElementNotInteractableException):
                self.logger.debug(f"click failure by adjusting position {-i}")
        self.logger.info("click failure by adjusting position")
        return False

    def _adjust_size(self, element: WebElement) -> bool:
        for size in env.WINDOW_SIZES_LARGE:
            self.logger.debug(f"changing window size to {size}")
            self.browser.set_window_size(*(w for w in size))
            try:
                element.click()
                self.logger.info(f"click successful by changing size to: {size}")
                return True
            except (ElementClickInterceptedException, ElementNotInteractableException):
                self.logger.debug(f"click failure by adjusting size to {size}")
        self.logger.info("click failure by adjusting size")
        self.browser.set_window_size(*(w for w in env.WINDOW_SIZE))
        return False

    def nav(self, url: str = None, full_url=False, force=False) -> None:
        if not full_url:
            url = url_convert(url)
        if self.browser.current_url != url or force:
            self.logger.debug(f"Navigating to: {url}")
            return self.browser.get(url)
        self.logger.debug(
            f"skipping navigation to {url} due to the browser already being there"
        )

    def get_element(self, locator: Tuple[By, str], fail=False) -> WebElement:
        expected_element = presence_of_element_located(locator)
        if fail:
            return self.browser.fail_wait.until(expected_element)
        return self.browser.wait.until(expected_element)

    def get_all_elements(self, locator: Tuple[By, str], fail=False) -> list[WebElement]:
        expected_elements = presence_of_all_elements_located(locator)
        if fail:
            return self.browser.fail_wait.until(expected_elements)
        return self.browser.wait.until(expected_elements)

    def input_text(self, element: WebElement, text: str) -> WebElement:
        element.clear()
        element.send_keys(text)

    @contextmanager
    def _click_errors(self, element: WebElement) -> None:
        try:
            yield
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
            if not self._click_error_retries(element, e):
                raise

    def click(self, element: WebElement) -> None:
        with self._click_errors(element):
            self.browser.wait.until(element_to_be_clickable(element))
            element.click()

    def send_enter(self, element: WebElement) -> None:
        element.send_keys(Keys.ENTER)

    def make_session_stale(
        self,
    ) -> None:  # used primarily to to test the 'remember me' setting
        self.browser.delete_cookie("session")
