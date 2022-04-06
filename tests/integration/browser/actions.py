from typing import Tuple
import pytest
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from selenium.webdriver.common.by import By

from tests.helpers._async import run_parallel, run_sequence

class BrowserActions:
    def __init__(self, brand: str, browser: webdriver.Chrome) -> None:
        self.brand = brand
        self.browser = browser

    def clear_cookies(self) -> None:
        self.browser.delete_all_cookies

    def make_session_stale(self) -> None:
        self.browser.delete_cookie("session")

    async def nav(self, url: str, next=None) -> None:
        if next is None:
            next = url
        self.browser.get(url)
        await self._confirm_nav(next)

    async def _confirm_nav(
        self, url: str, timeout: int = 10, partial_url: bool = False
    ):
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
        self, locator: Tuple[str, str], timeout: int = 10, is_hidden: bool = False
    ) -> WebElement:
        el = WebDriverWait(self.browser, timeout).until(
            expected_conditions.presence_of_element_located(locator)
        )
        assert el.is_displayed() != is_hidden
        return el

    async def input(self, element: WebElement, input_: str) -> WebElement:
        id_ = element.get_attribute("id")
        assert id_ is not None
        element.clear()
        element.send_keys(input_)
        updated = await self.get_element((By.ID, id_))
        assert input_ == updated.get_attribute("value")
        return updated

    def click(self, element: WebElement):
        element.click()

    async def submit(
        self, element: WebElement, next: str = None, partial_url=False
    ) -> None:
        current = self.browser.current_url
        element.send_keys(Keys.ENTER)
        if next is not None:
            await self._confirm_nav(next, partial_url=partial_url)
        else:
            await self._confirm_nav(current, partial_url=partial_url)

    async def anon_nav(self):

        await self._nav_exists()
        await run_parallel(
            self.get_element((By.XPATH, "//a[@href='/']")),
            self.get_element((By.XPATH, "//a[@href='/register']")),
        )

    async def auth_nav(self):

        await self._nav_exists()
        await run_parallel(
            self.get_element((By.XPATH, "//a[@href='/logout']")),
            self.get_element((By.XPATH, "//a[@href='/profile']")),
            self.get_element((By.XPATH, "//a[@href='/bugs']")),
        )

    async def _nav_exists(self):

        await run_parallel(
            self.get_element((By.TAG_NAME, "nav")),
            self.get_element((By.XPATH, "//a[@href='/index']")),
        )
        with pytest.raises(TimeoutException):
            await self.get_element((By.XPATH, "//a[@href='/admin']"), timeout=0.2)
