from selenium.common.exceptions import TimeoutException

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