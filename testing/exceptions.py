from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement


class CharacterMissingError(Exception):
    def __init__(self, name: str, elements: list[WebElement], *args: object) -> None:
        super().__init__(*args)
        self.name = name
        self.elements = elements

    def __str__(self) -> str:
        return f"{self.name} not found in {[el.text for el in self.elements]}"

class ExpectedException(Exception):
    pass

class GameNotFoundError(Exception):
    pass

class ExpectedAmountError(AssertionError):
    pass

class ExpectedTextNotFoundError(AssertionError):
    pass

class DifferentURLError(TimeoutException):
    pass

class ElementNotFoundError(TimeoutException):
    pass