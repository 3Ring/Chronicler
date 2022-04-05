import pytest
from tests.fixtures.integration.browser.base import BrowserActions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def anon_nav(browser: BrowserActions):
    _nav_exists(browser)
    browser.get_element((By.XPATH, "//a[@href='/']"))
    browser.get_element((By.XPATH, "//a[@href='/register']"))

def auth_nav(browser: BrowserActions):
    _nav_exists(browser)
    browser.get_element((By.XPATH, "//a[@href='/logout']"))
    browser.get_element((By.XPATH, "//a[@href='/profile']"))
    browser.get_element((By.XPATH, "//a[@href='/bugs']"))

def _nav_exists(browser: BrowserActions):
    browser.get_element((By.TAG_NAME, "nav"))
    browser.get_element((By.XPATH, "//a[@href='/index']"))
    with pytest.raises(NoSuchElementException):
        browser.get_element((By.XPATH, "//a[@href='/admin']"), timeout=1)
