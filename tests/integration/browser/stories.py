import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from tests.integration.browser.actions import BrowserActions
from tests.helpers.all import chron_url
from io import TextIOWrapper
from tests.helpers.all import generate_game
from project.helpers.misc import bool_convert
from tests.helpers._async import run_parallel


class BrowserStories(BrowserActions):
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

        name = name if name is not None else self.name
        email = email if email is not None else self.email
        password = password if password is not None else self.password
        confirm = confirm if confirm is not None else self.confirm

        await self.nav(chron_url("/register"))
        (reg_name, reg_email, reg_password, reg_confirm,) = await run_parallel(
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

        name, dm_submit = await run_parallel(
            self.get_element((By.XPATH, "//input[@name='name']")),
            self.get_element((By.ID, "submit")),
        )
        if dm_name is not None:
            await self.input(name, dm_name)
        await self.submit(dm_submit, next=chron_url("/notes"), partial_url=True)

    async def logout(self):
        await self.nav(chron_url("/logout"), next=chron_url())

    async def reauth(self, restricted: str):

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
        restricted = "/edit/account"
        self.browser.delete_cookie("session")
        await self.nav(chron_url("/profile/account", next=restricted))
        edit = await self.get_element((By.XPATH, "//a[@href='/edit/account']"))
        await self.submit(edit, next=chron_url("/reauth", next=restricted))
        return restricted

    # async def login_with_game(self, games: list[dict] = None):
    #     games = games if games is not None else [generate_game(self.fp)]
    #     await asyncio.create_task(self.register())
    #     await asyncio.create_task(self.login())
    #     for game in games:
    #         await asyncio.create_task(self.create_game(game))
