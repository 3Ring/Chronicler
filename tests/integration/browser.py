from logging import exception
from typing import Tuple

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException

# Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Firefox
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Edge
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions

from selenium.webdriver.remote.webelement import WebElement

# import threading
# thread_local = threading.local()

class Browsers:
    @staticmethod
    def chrome():
        print(f'm1')
        browser = Chrome()
        print(f'm2')
        browser.browser_type = "chrome"
        print(f'm3')
        # options = ChromeOptions()
        # print(f'm4')
        # options.headless = True
        # print(f'm5')
        # # manager = await 
        # service = ChromeService(ChromeDriverManager().install())
        # print(f'm6')
        # browser.driver = webdriver.Chrome(options=options, service=service)
        # print(f'm7')
        # if not hasattr(thread_local, "browser"):
        #     thread_local.browser = browser
        # print(f'm8')
        return browser
        # return browser

    # async def make_chrome():
    #     ChromeService(ChromeDriverManager().install())
    #     webdriver.Chrome(options=options, service=service)
    # # @staticmethod
    # def firefox():
    #     return Firefox()

    # @staticmethod
    # def edge():
    #     return Edge()


class BrowserBase:
    # this is just for intellisense. it's not necessarily a Chrome driver, but they all share most methods
    driver: webdriver.Chrome

    def _nav_exists(self):
        self.get_element((By.TAG_NAME, "nav"))
        self.get_element((By.XPATH, "//a[@href='/index']"))
        with pytest.raises(NoSuchElementException):
            self.get_element((By.XPATH, "//a[@href='/admin']"), timeout=1)

    def anon_nav(self):
        self._nav_exists()
        self.get_element((By.XPATH, "//a[@href='/']"))
        self.get_element((By.XPATH, "//a[@href='/register']"))

    def auth_nav(self):
        self._nav_exists()
        self.get_element((By.XPATH, "//a[@href='/logout']"))
        self.get_element((By.XPATH, "//a[@href='/profile']"))
        self.get_element((By.XPATH, "//a[@href='/bugs']"))

    def get_element(self, locator: Tuple[str, str], timeout: int = 10, is_hidden: bool = False) -> WebElement:
        # print(f'in get element::: self.driver.current_url: {self.driver.current_url}')
        el = WebDriverWait(self.driver, timeout).until(
            expected_conditions.presence_of_element_located(locator)
        )
        assert el.is_displayed() != is_hidden
        return el

    def submit(self, element: WebElement, next: str = None, partial_url=False) -> None:
        current = self.driver.current_url
        # print(f'element: {element.is_displayed()}')
        element.send_keys(Keys.ENTER)
        if next is not None:
            self._confirm_nav(next, partial_url=partial_url)
        else:
            self._confirm_nav(current, partial_url=partial_url)

    def nav(self, url: str, next=None) -> None:
        if next is None:
            next = url
        self.driver.get(url)
        self._confirm_nav(next)

    def _confirm_nav(self, url: str, timeout: int = 10, partial_url: bool=False):
        try:
            if partial_url:
                WebDriverWait(self.driver, timeout).until(
                    expected_conditions.url_contains(url)
                )
            else:
                WebDriverWait(self.driver, timeout).until(
                    expected_conditions.url_to_be(url)
                )
        except Exception as e:
            print(f"currrent url is: {self.driver.current_url}. expected is: {url}")
            raise e

    def input(self, element: WebElement, input_: str) -> WebElement:

        id_ = element.get_attribute("id")
        assert id_ is not None
        element.clear()
        element.send_keys(input_)
        updated = self.get_element((By.ID, id_))
        assert input_ == updated.get_attribute("value")
        return updated

    def click(self, element: WebElement):
        element.click()


class Chrome(BrowserBase):
    def __init__(self):
        self.browser_type = "chrome"
        options = ChromeOptions()
        options.headless = True
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(options=options, service=service)


class Firefox(BrowserBase):
    def __init__(self):
        self.browser_type = "firefox"
        options = FirefoxOptions()
        options.headless = True
        service = FirefoxService(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(options=options, service=service)


class Edge(BrowserBase):
    def __init__(self):
        self.browser_type = "edge"
        options = EdgeOptions()
        options.headless = True
        service = EdgeService(EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(options=options, service=service)

        # self.driver.delete_cookie()
