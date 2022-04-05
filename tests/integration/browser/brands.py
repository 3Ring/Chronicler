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


import asyncio


class Browsers:
    supported = ["chrome", "firefox", "edge"]

    def __init__(self, brand) -> None:
        if brand not in self.supported:
            raise NotImplementedError(
                f"""{brand} is not implimented. Use {'" or "'.join(self.supported)}"""
            )
        self.brand = brand

    async def get(self) -> webdriver.Chrome:
        return await getattr(self, self.brand)()

    async def chrome(self) -> webdriver.Chrome:
        options = await asyncio.to_thread(ChromeOptions)
        options.headless = True
        a = await asyncio.to_thread(ChromeDriverManager)
        b = await asyncio.to_thread(a.install)
        service = await asyncio.to_thread(ChromeService, b)
        driver = await asyncio.to_thread(
            webdriver.Chrome, options=options, service=service
        )
        assert driver is not None
        return {"driver": driver, "brand": "chrome"}

    async def firefox(self) -> webdriver.Firefox:
        options = await asyncio.to_thread(FirefoxOptions)
        options.headless = True
        a = await asyncio.to_thread(GeckoDriverManager)
        b = await asyncio.to_thread(a.install)
        service = await asyncio.to_thread(FirefoxService, b)
        driver = await asyncio.to_thread(
            webdriver.Firefox, options=options, service=service
        )
        assert driver is not None
        return {"driver": driver, "brand": "firefox"}

    async def edge(self) -> webdriver.Edge:
        options = await asyncio.to_thread(EdgeOptions)
        options.headless = True
        a = await asyncio.to_thread(EdgeChromiumDriverManager)
        b = await asyncio.to_thread(a.install)
        service = await asyncio.to_thread(EdgeService, b)
        driver = await asyncio.to_thread(
            webdriver.Edge, options=options, service=service
        )
        assert driver is not None
        return {"driver": driver, "brand": "edge"}
