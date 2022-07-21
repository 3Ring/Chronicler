from __future__ import annotations



from dataclasses import dataclass
from typing import Tuple

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import url_contains, url_to_be

from testing.end_to_end.browser.ui import BrowserUI
from testing.end_to_end.helpers import url_convert
from testing.globals import LOGGER

@dataclass
class CheckActions:
    ui: BrowserUI

    def confirm_url(self, url: str, partial_url: bool = False, full_url: bool = False):
        if not full_url:
            url = url_convert(url)
        try:
            if partial_url:
                return self.ui.browser.wait.until(url_contains(url))
            return self.ui.browser.wait.until(url_to_be(url))

        except TimeoutException:
            LOGGER.file.error(
                "Originating in actions/check_actions/CheckActions.confirm_url:\n"
                + f"-intended url: {url}\n"
                + f"-current_url is: {self.ui.browser.current_url}\n"
                + f"-partial url: {partial_url}\n"
                + f"-full url: {full_url}"
            )
            raise

    def nav_is_anon(self):
        """confirms that the nav bar exists and contains the correct links for an anonymous user"""
        self._nav_exists()

        self.ui.get_element((By.CSS_SELECTOR, "a[href='/']"))
        self.ui.get_element((By.CSS_SELECTOR, "a[href='/register']"))
        for selector in ["a[href='/logout']", "a[href='/profile']", "a[href='/bugs']"]:
            with pytest.raises(TimeoutException):
                self.ui.get_element((By.CSS_SELECTOR, selector), fail=True)

    def nav_is_authenticated(self):
        """confirms that the nav bar exists and contains the correct links for a logged-in user"""
        self._nav_exists()
        self.ui.get_element((By.CSS_SELECTOR, "a[href='/logout']"))
        self.ui.get_element((By.CSS_SELECTOR, "a[href='/profile']"))
        self.ui.get_element((By.CSS_SELECTOR, "a[href='/bugs']"))

    def _nav_exists(self):
        """confirms that the nav bar exists and contains the base items"""
        self.ui.get_element((By.TAG_NAME, "nav"))
        self.ui.get_element((By.CSS_SELECTOR, "a[href='/index']"))
        with pytest.raises(TimeoutException):
            self.ui.get_element((By.CSS_SELECTOR, "[href='/admin']"), fail=True)

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
        assert self.ui.get_element(locator)

    def submit_and_check(
        self,
        element: WebElement,
        destination: str,
        partial_url: bool = False,
    ) -> None:
        self.ui.click(element)
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
            url = self.ui.browser.current_url
        self.ui.click(link)
        self.confirm_url(url, partial_url=partial_url)
