from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, List

if TYPE_CHECKING:
    from testing.end_to_end.browser import TestsBrowser

import os
from contextlib import contextmanager

import pytest
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import (
    presence_of_all_elements_located,
    presence_of_element_located,
    element_to_be_clickable,
    url_contains,
    url_to_be,
)
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    TimeoutException,
)

from testing.end_to_end.helpers import redirect, url_convert
from testing import globals as env
from testing.globals import LOGGER
from testing import exceptions as ex


class BrowserUI:
    def __init__(self, browser: TestsBrowser) -> None:
        self.browser = browser

    def _click_error_retries(self, element: WebElement, ex: Exception):
        LOGGER.info(f"{ex.__class__}: {ex.msg}\nAttempting fix by adjusting position")
        if self._adjust_position(element):
            return True
        LOGGER.info("Attempting fix by adjusting size")
        return self._adjust_size(element)

    def _adjust_position(self, element: WebElement) -> bool:
        for index, i in enumerate(([20] * 5)):
            LOGGER.debug(f"adjusting page position by {-index}")
            self.browser.set_window_position(0, -i)
            try:
                element.click()
                LOGGER.info(f"click successful by adjusting position by {-i}")
                return True
            except (ElementClickInterceptedException, ElementNotInteractableException):
                LOGGER.debug(f"click failure by adjusting position {-i}")
        LOGGER.info("click failure by adjusting position")
        return False

    def _adjust_size(self, element: WebElement) -> bool:
        for size in env.WINDOW_DEBUG_SIZES:
            LOGGER.debug(f"changing window size to {size}")
            self.browser.set_window_size(*(w for w in size))
            try:
                self._adjust_position(element)
                LOGGER.info(f"click successful by changing size to: {size}")
                return True
            except (ElementClickInterceptedException, ElementNotInteractableException):
                LOGGER.debug(f"click failure by adjusting size to {size}")
        LOGGER.info("click failure by adjusting size")
        self.browser.set_window_size(*(w for w in env.WINDOW_SIZE))
        return False

    def nav(self, url: str, full_url=False, force=False, confirm=False) -> None:
        """
        If the browser is not already at the url, navigate to the url

        :param url: sub-domain or full-url being navigated to
        :param full_url: set to True if not a sub-domain. defaults to False
        :param force: If True, will force the browser to navigate to the url even if it's already there,
        defaults to False
        """
        if not full_url:
            url = url_convert(url)
        if self.browser.current_url != url or force:
            LOGGER.debug(f"Navigating to: {url}")
            return self.browser.get(url)
        LOGGER.debug(
            f"skipping navigation to {url} due to the browser already being there"
        )
        if confirm:
            self.confirm_url(url, full_url=True)

    def chronicler_url(self, url: str = None) -> str:
        """gets releative url with domain striped away
        if url is none: use current url
        """
        if url is None:
            url = self.browser.current_url
        if url.find(os.environ.get("ROOT_URL")) != -1:
            return url[len(os.environ.get("ROOT_URL")) :]
        return url

    def get_element(self, locator: Tuple[By, str], fail=False) -> WebElement:
        """gets element from current page. raises exception if not found"""
        try:
        expected_element = presence_of_element_located(locator)
        if fail:
            return self.browser.fail_wait.until(expected_element)
        return self.browser.wait.until(expected_element)
        except TimeoutException:
            raise ex.ElementNotFoundError(
                f"unable to find elements by locator: {locator} on {self.browser.current_url}"
            )

    def get_all_elements(self, locator: Tuple[By, str], fail=False) -> List[WebElement]:
        try:
        expected_elements = presence_of_all_elements_located(locator)
        if fail:
            return self.browser.fail_wait.until(expected_elements)
        return self.browser.wait.until(expected_elements)
        except TimeoutException:
            raise ex.ElementNotFoundError(
                f"unable to find elements by locator: {locator} on {self.browser.current_url}"
            )

    def input_text(
        self, element: WebElement, text: str, no_clear: bool = False
    ) -> WebElement:
        """clears the current text and sends new text"""
        if not no_clear:
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

    #
    # checks
    #
    def confirm_url(self, url: str, partial_url: bool = False, full_url: bool = False):
        if not full_url:
            url = url_convert(url)
        try:
            if partial_url:
                return self.browser.wait.until(url_contains(url))
            return self.browser.wait.until(url_to_be(url))

        except TimeoutException:
            LOGGER.file.error(
                "Originating in actions/check_actions/CheckActions.confirm_url:\n"
                + f"-intended url: {url}\n"
                + f"-current_url is: {self.browser.current_url}\n"
                + f"-partial url: {partial_url}\n"
                + f"-full url: {full_url}"
            )
            raise ex.DifferentURLError(
                f"current url: {self.browser.current_url} is not {url}"
            )

    def nav_is_anon(self):
        """confirms that the nav bar exists and contains the correct links for an anonymous user"""
        self._nav_exists()

        self.get_element((By.CSS_SELECTOR, "a[href='/']"))
        self.get_element((By.CSS_SELECTOR, "a[href='/register']"))
        for selector in ["a[href='/logout']", "a[href='/profile']", "a[href='/bugs']"]:
            with pytest.raises(ex.ElementNotFoundError):
                self.get_element((By.CSS_SELECTOR, selector), fail=True)

    def nav_is_authenticated(self):
        """confirms that the nav bar exists and contains the correct links for a logged-in user"""
        self._nav_exists()
        self.get_element((By.CSS_SELECTOR, "a[href='/logout']"))
        self.get_element((By.CSS_SELECTOR, "a[href='/profile']"))
        self.get_element((By.CSS_SELECTOR, "a[href='/bugs']"))

    def _nav_exists(self):
        """confirms that the nav bar exists and contains the base items"""
        self.get_element((By.TAG_NAME, "nav"))
        self.get_element((By.CSS_SELECTOR, "a[href='/index']"))
        with pytest.raises(ex.ElementNotFoundError):
            self.get_element((By.CSS_SELECTOR, "[href='/admin']"), fail=True)

    def has_attributes(self, element: WebElement, attrs: dict) -> None:
        """
        confirms element has attribute key/value pairs

        Set value to be "_any" if any value should pass.
        ex: self.assert_attributes(element, data_flag="_any") will only check that the attribute is present

        :param element: Webelement element to check
        :param attrs: dict containing the key/value pairs to check
        """
        for attr_name, value in attrs.items():
            attr_value = element.get_attribute(attr_name)
            if value == "_any":
                assert attr_value is not None
            else:
                assert attr_value == value

    def element_exists(self, locator: Tuple[By, str]) -> None:
        assert self.get_element(locator)

    def submit_and_check(
        self,
        element: WebElement,
        destination: str,
        partial_url: bool = False,
    ) -> None:
        self.click(element)
        self.confirm_url(destination, partial_url=partial_url)

    def click_link_and_confirm(
        self, link: WebElement, url: str = None, partial_url: bool = False
    ) -> None:
        """
        > Click a link and confirm that the URL you are directed to is correct

        :param link: WebElement - the link to click
        :param url: The URL that you want to confirm
        """
        if url is None:
            url = self.chronicler_url(self.browser.current_url)
        self.click(link)
        self.confirm_url(url, partial_url=partial_url)
