import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

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

from testing.globals import WINDOW_SIZE


class TestsBrowser(WebDriver):
    wait: WebDriverWait
    fail_wait: WebDriverWait


class TestsChrome(webdriver.Chrome, TestsBrowser):
    def __init__(
        self,
        wait: WebDriverWait,
        fail_wait: WebDriverWait,
        executable_path=...,
        port=...,
        options: ChromeOptions = None,
        service_args=None,
        desired_capabilities=None,
        service_log_path=...,
        chrome_options=None,
        service: ChromeService = None,
        keep_alive=...,
    ):
        super().__init__(
            executable_path,
            port,
            options,
            service_args,
            desired_capabilities,
            service_log_path,
            chrome_options,
            service,
            keep_alive,
        )
        self.wait = wait
        self.fail_wait = fail_wait


class TestsFirefox(webdriver.Firefox, TestsBrowser):
    def __init__(
        self,
        wait: WebDriverWait,
        fail_wait: WebDriverWait,
        firefox_profile=None,
        firefox_binary=None,
        capabilities=None,
        proxy=None,
        executable_path=...,
        options: FirefoxOptions = None,
        service_log_path=...,
        service_args=None,
        service: FirefoxService = None,
        desired_capabilities=None,
        log_path=...,
        keep_alive=True,
    ):
        super().__init__(
            firefox_profile,
            firefox_binary,
            capabilities,
            proxy,
            executable_path,
            options,
            service_log_path,
            service_args,
            service,
            desired_capabilities,
            log_path,
            keep_alive,
        )
        self.wait = wait
        self.fail_wait = fail_wait


class TestsEdge(webdriver.Edge, TestsBrowser):
    def __init__(
        self,
        wait: WebDriverWait,
        fail_wait: WebDriverWait,
        executable_path=...,
        port=...,
        options: EdgeOptions = ...,
        service_args=None,
        capabilities=None,
        service_log_path=...,
        service: EdgeService = None,
        keep_alive=False,
        verbose=False,
    ):
        super().__init__(
            executable_path,
            port,
            options,
            service_args,
            capabilities,
            service_log_path,
            service,
            keep_alive,
            verbose,
        )
        self.wait = wait
        self.fail_wait = fail_wait


class BrowserInitializer:
    @staticmethod
    def chrome(
        wait: WebDriverWait, fail_wait: WebDriverWait, log_level: int
    ) -> TestsChrome:
        """
        Create and return a Chrome webdriver with headless options
        """
        options = ChromeOptions()
        options.headless = True
        options.add_argument("start-maximized")
        manager = ChromeDriverManager(log_level=log_level)
        service = ChromeService(manager.install())
        driver = TestsChrome(
            wait=wait, fail_wait=fail_wait, options=options, service=service
        )
        driver.set_window_size(*(w for w in WINDOW_SIZE))
        driver.wait._driver = driver
        driver.fail_wait._driver = driver
        assert driver is not None
        return driver

    @staticmethod
    def firefox(
        wait: WebDriverWait, fail_wait: WebDriverWait, log_level: int
    ) -> TestsBrowser:
        """
        Create and return a Firefox webdriver with headless options
        """
        options = FirefoxOptions()
        options.headless = True
        options.add_argument("start-maximized")
        manager = GeckoDriverManager(log_level=log_level)
        service = FirefoxService(manager.install(), log_path=None)
        driver = TestsFirefox(
            wait=wait, fail_wait=fail_wait, options=options, service=service
        )
        driver.set_window_size(*(w for w in WINDOW_SIZE))
        driver.wait._driver = driver
        driver.fail_wait._driver = driver
        assert driver is not None
        return driver

    @staticmethod
    def edge(
        wait: WebDriverWait, fail_wait: WebDriverWait, log_level: int
    ) -> TestsBrowser:
        """
        Create and return an Edge webdriver with headless options
        """
        options = EdgeOptions()
        options.headless = True
        options.add_argument("start-maximized")
        manager = EdgeChromiumDriverManager(log_level=log_level)
        service = EdgeService(manager.install())
        # !bug explicitly putting in the path here is a workaround because webdriver_manager has a bug.
        driver = TestsEdge(
            executable_path="C:/Users/celes/Desktop/edge_driver/msedgedriver.exe",
            wait=wait,
            fail_wait=fail_wait,
            options=options,
            service=service,
        )
        driver.set_window_size(*(w for w in WINDOW_SIZE))
        driver.wait._driver = driver
        driver.fail_wait._driver = driver
        assert driver is not None
        return driver
