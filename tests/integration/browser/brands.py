from selenium import webdriver

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


class Browsers:
    """This is a factory class that creates a webdriver object based on the brand of browser."""
    supported = ["chrome", "firefox", "edge"]

    def __init__(self, brand) -> None:
        if brand not in self.supported:
            raise NotImplementedError(
                f"""{brand} is not implimented. Use {'" or "'.join(self.supported)}"""
            )
        self.brand = brand

    def get(self) -> webdriver.Chrome:
        """returns a webdriver object."""
        return getattr(self, self.brand)()

    def chrome(self) -> webdriver.Chrome:
        """
        Create a Chrome webdriver with headless options
        :return: A dictionary with the driver and the brand of the browser.
        """
        options = ChromeOptions()
        options.headless = True
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(options=options, service=service)
        assert driver is not None
        return {"driver": driver, "brand": "chrome"}

    def firefox(self) -> webdriver.Firefox:
        """
        Create a Firefox webdriver with headless options
        :return: A dictionary with the driver and the brand of the browser.
        """
        options = FirefoxOptions()
        options.headless = True
        service = FirefoxService(GeckoDriverManager().install(), log_path=None)
        driver = webdriver.Firefox(options=options, service=service)
        assert driver is not None
        return {"driver": driver, "brand": "firefox"}

    def edge(self) -> webdriver.Edge:
        """
        Create an Edge webdriver with headless options
        :return: A dictionary with the driver and the brand of the browser.
        """
        options = EdgeOptions()
        options.headless = True
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(options=options, service=service)
        assert driver is not None
        return {"driver": driver, "brand": "edge"}
