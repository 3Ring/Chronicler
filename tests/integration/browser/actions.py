from typing import Tuple
import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from tests.helpers._async import run_parallel


class BrowserActions:
    """A class containing all the low level methods for navigating around the test server"""

    def __init__(self, brand: str, browser: webdriver.Chrome) -> None:
        self.brand = brand
        self.browser = browser

    def clear_cookies(self) -> None:
        self.browser.delete_all_cookies

    def make_session_stale(self) -> None:
        """used primarily to to test the 'remember me' setting"""
        self.browser.delete_cookie("session")

    async def nav(self, url: str, next=None) -> None:
        """
        The function navigates to a url and confirms that the browser has navigated to the correct url

        :param url: The URL to navigate to
        :param next: The URL where the browser will be redirected to
        """
        if next is None:
            next = url
        self.browser.get(url)
        await self._confirm_nav(next)

    async def _confirm_nav(
        self, url: str, timeout: int = 10, partial_url: bool = False
    ):
        """
        Wait for the URL to be the expected URL

        :param url: The URL to navigate to
        :param timeout: The amount of time we’re willing to wait for our target element to be found,
        defaults to 10
        :param partial_url: If you want to wait for a partial url, for example, if you want to wait for
        https://www.google.com/search?q=test, you can set partial_url=True, defaults to False
        """
        try:
            if partial_url:
                WebDriverWait(self.browser, timeout).until(
                    expected_conditions.url_contains(url)
                )
            else:
                WebDriverWait(self.browser, timeout).until(
                    expected_conditions.url_to_be(url)
                )
        except Exception as e:
            print(f"currrent url is: {self.browser.current_url}. expected is: {url}")
            raise e

    async def get_element(
        self, locator: Tuple[By, str], timeout: int = 10, is_hidden: bool = False
    ) -> WebElement:
        """
        Wait for the element to be present in the DOM and return its The WebElement object.

        :param locator: A tuple of the form (by, selector) where by is a By class and selector is a string
        :param timeout: The amount of time to wait for the element to be visible, defaults to 10
        :param is_hidden: If True, the element is expected to be hidden, defaults to False
        :return: The WebElement object.
        """
        el = WebDriverWait(self.browser, timeout).until(
            expected_conditions.presence_of_element_located(locator)
        )
        assert el.is_displayed() != is_hidden
        return el

    async def input(self, element: WebElement, input_: str) -> WebElement:
        """
        Input the given element with the given input_ and return the updated element

        :param element: The element to input into
        :param input_: The text to input into the element
        :return: WebElement
        """
        id_ = element.get_attribute("id")
        assert id_ is not None
        element.clear()
        element.send_keys(input_)
        updated = await self.get_element((By.ID, id_))
        assert input_ == updated.get_attribute("value")
        return updated

    def click(self, element: WebElement):
        """
        Click on the element

        :param element: The WebElement object that you want to click
        """
        element.click()

    async def submit(
        self, element: WebElement, next: str = None, partial_url=False
    ) -> None:
        """
        Submit a form by pressing the enter key

        :param element: The element to submit
        :param next: The URL expected to be redirected to after submitting the form
        :param partial_url: If True, the next URL will be only need to be in the final URL that the browser is redirected to. If False, the next
        URL will be checked exactly, defaults to False (optional)
        """
        current = self.browser.current_url
        element.send_keys(Keys.ENTER)
        if next is not None:
            await self._confirm_nav(next, partial_url=partial_url)
        else:
            await self._confirm_nav(current, partial_url=partial_url)

    async def anon_nav(self):
        """confirms that the nav bar exists and contains the correct links for an anonymous user"""

        await self._nav_exists()
        await run_parallel(
            self.get_element((By.XPATH, "//a[@href='/']")),
            self.get_element((By.XPATH, "//a[@href='/register']")),
        )
        with pytest.raises(TimeoutException):
            await run_parallel(
                self.get_element((By.XPATH, "//a[@href='/logout']"), timeout=0.2),
                self.get_element((By.XPATH, "//a[@href='/profile']"), timeout=0.2),
                self.get_element((By.XPATH, "//a[@href='/bugs']"), timeout=0.2),
            )

    async def auth_nav(self):
        """confirms that the nav bar exists and contains the correct links for an logged-in user"""
        await self._nav_exists()
        await run_parallel(
            self.get_element((By.XPATH, "//a[@href='/logout']")),
            self.get_element((By.XPATH, "//a[@href='/profile']")),
            self.get_element((By.XPATH, "//a[@href='/bugs']")),
        )

    async def _nav_exists(self):
        """confirms that the nav bar exists and contains the base items"""
        await run_parallel(
            self.get_element((By.TAG_NAME, "nav")),
            self.get_element((By.XPATH, "//a[@href='/index']")),
        )
        with pytest.raises(TimeoutException):
            await self.get_element((By.XPATH, "//a[@href='/admin']"), timeout=0.2)
