from io import TextIOWrapper
from selenium import webdriver
from selenium.webdriver.common.by import By

from tests.integration.browser.actions import BrowserActions
from tests.helpers.all import chron_url
from project.helpers.misc import bool_convert
from tests.helpers._async import run_parallel


class BrowserStories(BrowserActions):
    """A class containing all high level methods for navigating around the test server"""

    def __init__(self, brand: str, browser: webdriver.Chrome) -> None:
        super().__init__(brand=brand, browser=browser)

    async def register(
        self,
        name: str = None,
        email: str = None,
        password: str = None,
        confirm: str = None,
        fail: bool = False,
    ):
        """
        registers a user.

        :param name: The name to register with
        :param email: The email address to register with
        :param password: The password to use for the registration
        :param confirm: The password confirmation
        :param fail: If True, the registration will fail. Otherwise, it will succeed, defaults to False
        """
        name = name if name is not None else self.name
        email = email if email is not None else self.email
        password = password if password is not None else self.password
        confirm = confirm if confirm is not None else self.confirm
        await self.nav(chron_url("/register"))
        reg_name, reg_email, reg_password, reg_confirm = await run_parallel(
            self.get_element((By.XPATH, "//input[@name='name']")),
            self.get_element((By.XPATH, "//input[@name='email']")),
            self.get_element((By.XPATH, "//input[@name='password']")),
            self.get_element((By.XPATH, "//input[@name='confirm']")),
        )
        await run_parallel(
            self.input(reg_name, name),
            self.input(reg_email, email),
            self.input(reg_password, password),
            self.input(reg_confirm, confirm),
        )
        reg_form_submit = await self.get_element((By.ID, "usersubmit"))
        if fail:
            await self.submit(reg_form_submit, next=chron_url("/register"))
        else:
            await self.submit(reg_form_submit, next=chron_url())

    async def login(
        self,
        email: str = None,
        password: str = None,
        fail: bool = False,
        remember: bool = True,
    ):
        """
        logs in the user. (Will fail if not registered first)

        :param email: The email to use for logging in
        :param password: The password to user for loggin in
        :param fail: If True, the login will fail. If False, the login will succeed, defaults to False
        :param remember: If True, the login form will have a checkbox to "remember me", defaults to True
        """
        email = email if email is not None else self.email
        password = password if password is not None else self.password

        await self.nav(chron_url())
        login_email, login_password, login_submit, remember_me = await run_parallel(
            self.get_element((By.XPATH, "//input[@name='email']")),
            self.get_element((By.XPATH, "//input[@name='password']")),
            self.get_element((By.XPATH, "//input[@name='submit']")),
            self.get_element((By.XPATH, "//input[@name='remember']")),
        )
        if remember:
            remember_me.click()
        await run_parallel(
            self.input(login_email, email),
            self.input(login_password, password),
        )
        if fail == True:
            await self.submit(login_submit, next=chron_url())
        else:
            await self.submit(login_submit, next=chron_url("/index"))

    def reset(self, fp: TextIOWrapper) -> None:
        """Reset the browser to the initial state with new user information"""
        from tests.conftest import make_mock

        self.browser.delete_all_cookies()
        user = make_mock(fp=fp)
        self.template = user
        self.id = user.id
        self.name = user.name
        self.email = user.email
        self.password = user.password
        self.confirm = user.confirm

    async def create_game(self, game: dict, dm_name: bool = None) -> None:
        """Create a game and a DM for it

        :param game: the game parameters
        :param dm_name: The name of the DM
        """

        dm_name = dm_name if dm_name is not None else f"DM{self.name}"
        game["dm_name"] = dm_name
        self.games.append(game)

        await self.nav(chron_url("/create/game"))
        name, pub, game_submit = await run_parallel(
            self.get_element((By.ID, "name")),
            self.get_element((By.XPATH, "//input[@name='published']")),
            self.get_element((By.XPATH, "//input[@name='gamesubmit']")),
        )
        await self.input(name, game["name"])
        if game["publish"]:
            self.click(pub)
        assert bool_convert(pub.get_attribute("checked")) == game["publish"]
        await self.submit(game_submit, next=chron_url("/create/dm"), partial_url=True)
        await self.create_dm(game, dm_name)

    async def create_dm(self, dm_name: bool = None) -> None:
        """
        Create DM for new game. (Used for DM creation upon initial game creation)

        :param dm_name: The name of the DM you want to create
        """

        name, dm_submit = await run_parallel(
            self.get_element((By.XPATH, "//input[@name='name']")),
            self.get_element((By.ID, "submit")),
        )
        if dm_name is not None:
            await self.input(name, dm_name)
        await self.submit(dm_submit, next=chron_url("/notes"), partial_url=True)

    async def logout(self):
        """Logout the user by navigating to the logout page"""
        await self.nav(chron_url("/logout"), next=chron_url())

    async def reauth(self, restricted: str):
        """re-authenticates the user.

        :param restricted: the URL of the page expected to redirect to
        """

        email, password, submit = await run_parallel(
            self.get_element((By.XPATH, "//input[@name='email']")),
            self.get_element((By.XPATH, "//input[@name='password']")),
            self.get_element((By.XPATH, "//input[@name='submit']")),
        )
        await run_parallel(
            self.input(email, self.email),
            self.input(password, self.password),
        )
        await self.submit(submit, next=chron_url(restricted))

    async def forced_to_reauth(self):
        """force a stale session state and navigate the user to /edit/account which will force a re-authorization"""
        restricted = "/edit/account"
        self.browser.delete_cookie("session")
        await self.nav(chron_url("/profile/account", next=restricted))
        edit = await self.get_element((By.XPATH, "//a[@href='/edit/account']"))
        await self.submit(edit, next=chron_url("/reauth", next=restricted))
        return restricted
