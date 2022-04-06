from tests.integration.browser.stories import BrowserStories
from selenium import webdriver


class MockUser:

    games: list

    def __init__(
        self,
        _id: int,
        name: str = None,
        email: str = None,
        password: str = None,
        confirm: str = None,
    ) -> None:
        self.id = _id
        self.name = name if name is not None else f"User{self.id}"
        self.email = email if email is not None else f"User{self.id}@email.com"
        self.password = (
            password
            if password is not None
            else f"User{self.id}password!@#$%^&*()-=./,'\""
        )
        self.confirm = confirm if confirm is not None else self.password


class Mock(BrowserStories):
    def __init__(
        self,
        brand: str,
        browser: webdriver.Chrome,
        user: MockUser,
    ) -> None:
        super().__init__(
            brand=brand, browser=browser
        )
        self.template = user
        self.id = user.id
        self.name = user.name
        self.email = user.email
        self.password = user.password
        self.confirm = user.confirm
        self.games = list()

