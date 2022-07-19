from dataclasses import dataclass
from selenium.webdriver.common.by import By

from _logging import Logger
from end_to_end.helpers import query_string_convert
from end_to_end.browser.ui import BrowserUI
from end_to_end.browser.actions.check_actions import CheckActions
from end_to_end.browser.actions.create_actions import CreateActions
from end_to_end.browser.actions.auth_actions import AuthActions
from end_to_end.assets import User, Game


@dataclass
class StoryActions:
    ui: BrowserUI
    logger: Logger
    user: User
    check: CheckActions
    auth: AuthActions
    create: CreateActions

    def register_and_login(self):
        self.auth.register()
        self.auth.login()

    def create_game_and_dm(
        self,
        game_name: str = None,
        publish: bool = True,
        dm_image_path: str = None,
        dm_name: str = None,
        game_image_path: str = None,
        default_dm_name: bool = False,
    ) -> Game:

        game = self.create.game_object(
            game_name=game_name,
            publish=publish,
            dm_image_path=dm_image_path,
            dm_name=dm_name,
            game_image_path=game_image_path,
        )
        self.create.game(game)
        self.create.dm(game.dm, default_dm_name)
        return game

    def forced_to_reauth(self):
        """force a stale session state and navigate the user to /edit/account which will force a re-authorization"""
        url = "/edit/account"
        self.ui.make_session_stale()
        self.ui.nav("/profile/account")
        account_link = self.ui.get_element((By.CSS_SELECTOR, f"a[href='{url}']"))
        redirect_url = "/reauth" + query_string_convert(next="/edit/account")
        self.check.submit_and_check(account_link, destination=redirect_url)
        return url
