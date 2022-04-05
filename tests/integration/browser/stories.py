import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from tests.integration.browser.actions import BrowserActions
from tests.helpers.all import chron_url
from urllib.parse import urlencode

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

        await asyncio.create_task(self.nav(chron_url("/register")))
        reg_name = await asyncio.create_task(
            self.get_element((By.XPATH, "//input[@name='name']"))
        )
        reg_email = await asyncio.create_task(
            self.get_element((By.XPATH, "//input[@name='email']"))
        )
        reg_password = await asyncio.create_task(
            self.get_element((By.XPATH, "//input[@name='password']"))
        )
        reg_confirm = await asyncio.create_task(
            self.get_element((By.XPATH, "//input[@name='confirm']"))
        )
        reg_form_submit = await asyncio.create_task(
            self.get_element((By.XPATH, "//input[@name='usersubmit']"))
        )
        await asyncio.create_task(self.input(reg_name, name))
        await asyncio.create_task(self.input(reg_email, email))
        await asyncio.create_task(self.input(reg_password, password))
        await asyncio.create_task(self.input(reg_confirm, confirm))
        if fail:
            await asyncio.create_task(
                self.submit(reg_form_submit, next=chron_url("/register"))
            )
        else:
            await asyncio.create_task(self.submit(reg_form_submit, next=chron_url()))

    async def login(
        self,
        email: str = None,
        password: str = None,
        fail: bool = False,
        remember: bool = True
    ):
        email = email if email is not None else self.email
        password = password if password is not None else self.password

        await asyncio.create_task(self.nav(chron_url()))
        login_email = await asyncio.create_task(
            self.get_element((By.XPATH, "//input[@name='email']"))
        )
        login_password = await asyncio.create_task(
            self.get_element((By.XPATH, "//input[@name='password']"))
        )
        login_submit = await asyncio.create_task(
            self.get_element((By.XPATH, "//input[@name='submit']"))
        )
        if remember:
            remember_me = await asyncio.create_task(
                self.get_element((By.XPATH, "//input[@name='remember']"))
            )
            remember_me.click()
        await asyncio.create_task(self.input(login_email, email))
        await asyncio.create_task(self.input(login_password, password))
        if fail == True:
            await asyncio.create_task(self.submit(login_submit, next=chron_url()))
        else:
            await asyncio.create_task(
                self.submit(login_submit, next=chron_url("/index"))
            )

    async def reset(self) -> None:
        self.browser.delete_all_cookies()
    # async def create_game(self, game: dict = None, dm_name: bool = None) -> None:
    #     print(f"c1")
    #     game = game if game is not None else generate_game(self.fp)
    #     dm_name = dm_name if dm_name is not None else f"DM{self.name}"

    #     await asyncio.create_task(self.nav(chron_url("/create/game")))
    #     print(f"c2")
    #     name = await asyncio.create_task(self.get_element((By.ID, "name")))
    #     print(f"c3")
    #     await asyncio.create_task(self.input(name, game["name"]))
    #     pub = await asyncio.create_task(
    #         self.get_element((By.XPATH, "//input[@name='published']"))
    #     )
    #     print(f"c4")
    #     if game["publish"]:
    #         await asyncio.create_task(self.click(pub))
    #     print(f"c5")
    #     assert bool_convert(pub.get_attribute("checked")) == game["publish"]
    #     game_submit = await asyncio.create_task(
    #         self.get_element((By.XPATH, "//input[@name='gamesubmit']"))
    #     )
    #     print(f"c6")
    #     await asyncio.create_task(
    #         self.submit(game_submit, next=chron_url("/create/dm"), partial_url=True)
    #     )
    #     print(f"c7")
    #     await asyncio.create_task(self.create_dm(game, dm_name))
    #     print(f"c8")

    # async def create_dm(self, dm_name: bool = None) -> None:
    #     if dm_name is not None:
    #         name = await asyncio.create_task(
    #             self.get_element((By.XPATH, "//input[@name='name']"))
    #         )
    #         await asyncio.create_task(self.input(name, dm_name))
    #     dm_submit = await asyncio.create_task(self.get_element((By.ID, "submit")))
    #     # print(f'd1')
    #     await asyncio.create_task(
    #         self.submit(dm_submit, next=chron_url("/notes"), partial_url=True)
    #     )
    #     # print(f'd2')
    #     # print(f'game_created.driver.current_url: {game_created.driver.current_url}')

    async def logout(self):
        await asyncio.create_task(self.nav(chron_url("/logout"), next=chron_url()))

    async def reauth(self, restricted: str):
        email = await asyncio.create_task(
            self.get_element((By.XPATH, "//input[@name='email']"))
        )
        password = await asyncio.create_task(
            self.get_element((By.XPATH, "//input[@name='password']"))
        )
        submit = await asyncio.create_task(
            self.get_element((By.XPATH, "//input[@name='submit']"))
        )
        await asyncio.create_task(self.input(email, self.email))
        await asyncio.create_task(self.input(password, self.password))
        await asyncio.create_task(
            self.submit(submit, next=chron_url(restricted))
            )

    async def forced_to_reauth(self):
        restricted = "/edit/account"
        self.browser.delete_cookie("session")
        await asyncio.create_task(self.nav(chron_url("/profile/account", next=restricted)))
        edit = await asyncio.create_task(
            self.get_element((By.XPATH, "//a[@href='/edit/account']"))
        )
        await asyncio.create_task(
            self.submit(edit, next=chron_url("/reauth", next=restricted))
            # self.submit(edit, next=chron_url("/reauth", next=f"/reauth/q{urlencode({'next': '/edit/account'})}"))
        )
        return restricted

    # async def login_with_game(self, games: list[dict] = None):
    #     games = games if games is not None else [generate_game(self.fp)]
    #     await asyncio.create_task(self.register())
    #     await asyncio.create_task(self.login())
    #     for game in games:
    #         await asyncio.create_task(self.create_game(game))
