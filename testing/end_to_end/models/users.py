from __future__ import annotations
from typing import TYPE_CHECKING, Iterator, ClassVar

if TYPE_CHECKING:
    from end_to_end.mock import Mock

from dataclasses import dataclass, field

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from testing.end_to_end.models import Games, Characters, DMs
from testing.end_to_end.helpers import query_string_convert
from testing import globals as env
from testing.globals import LOGGER

@dataclass
class Users:
    id: int = field(default=None, init=False)
    name: str = None
    email: str = None
    password: str = None
    different_confirm: str = None
    player_games: list = field(default_factory=list)
    dm_games: list = field(default_factory=list)
    characters: list = field(default_factory=list)


    def __post_init__(self):
        self._set_attrs()

    @staticmethod
    def default_email(id: int):
        return f"test{id}@test.com"

    @staticmethod
    def default_name(id: int):
        return f"test{id}"

    @staticmethod
    def default_password(id: int):
        return f"TestPassword{id}"

    def change_password(self, new: str) -> None:
        self.password = new
        self.different_confirm = new

    def create_game_and_dm(
        self,
        mock: Mock,
        game_name: str = None,
        publish: bool = True,
        dm_image_path: str = None,
        dm_name: str = None,
        game_image_path: str = None,
        default_dm_name: bool = False,
    ) -> Games:
        game = Games(name=game_name, publish=publish, image_path=game_image_path)
        dm = DMs(user=mock.user, game=game, name=dm_name, image_path=dm_image_path)
        self.create_game(mock, game)
        self.create_dm(mock, game, dm=dm, default_dm_name=default_dm_name)
        return game

    def create_character(
        self,
        mock: Mock,
        character: Characters = None,
        fail: bool = False,
    ) -> Characters:
        """creates the character in the mock and appends it to self.characters
        will create a basic character if one is not provided"""
        if character is None:
            character = Characters(player=self)
        mock.ui.nav(env.URL_CREATE_CHARACTER)
        form_name = mock.ui.get_element(
            (By.CSS_SELECTOR, "input[name='name'][type='text']")
        )
        form_bio = mock.ui.get_element((By.CSS_SELECTOR, "textarea[name='bio']"))
        form_submit = mock.ui.get_element((By.CSS_SELECTOR, "input[type='submit']"))

        mock.ui.input_text(form_name, character.name)
        mock.ui.input_text(form_bio, character.bio)
        if character.image_path is not None:
            form_image = mock.ui.get_element(
                (By.CSS_SELECTOR, "input[name='img'][type='file']")
            )
            form_image.send_keys(character.image_path)

        url = env.URL_CREATE_CHARACTER if fail else env.URL_PROFILE_CHARACTERS
        try:
            mock.check.submit_and_check(form_submit, url)
            self.player_games.append(character)
            return character
        except TimeoutException:
            if not fail:
                LOGGER.error(f'failing character: "{character}"')
            raise

    def create_dm(
        self,
        mock: Mock,
        game: Games,
        dm: DMs = None,
        default_dm_name: bool = False,
        fail=False,
    ) -> DMs:
        """game must be created already and must be already on the correct page"""
        if not dm:
            dm = DMs(user=self, game=game)
        form_name = mock.ui.get_element((By.CSS_SELECTOR, "input[type='text']"))
        form_image = mock.ui.get_element(
            (By.CSS_SELECTOR, "input[name='img'][type='file']")
        )
        form_submit = mock.ui.get_element((By.CSS_SELECTOR, "input[type='submit']"))

        if not default_dm_name:
            mock.ui.input_text(form_name, dm.name)
        if dm.image_path:
            form_image.send_keys(dm.image_path)
        url = env.URL_CREATE_DM if fail else env.URL_NOTES
        try:
            mock.check.submit_and_check(form_submit, url, partial_url=True)
            game.dm = dm
            return dm
        except TimeoutException:
            if not fail:
                LOGGER.error(f'failing dm: "{dm}"')
            raise

    def create_game(self, mock: Mock, game: Games = None, fail: bool = False) -> Games:
        if not game:
            game = Games()
        mock.ui.nav(env.URL_CREATE_GAME)
        form_name = mock.ui.get_element(
            (By.CSS_SELECTOR, "input[type='text'][name='name']")
        )
        form_image = mock.ui.get_element((By.CSS_SELECTOR, "input[type='file']"))
        form_publish = mock.ui.get_element((By.CSS_SELECTOR, "input[name='published']"))
        form_submit = mock.ui.get_element((By.CSS_SELECTOR, "input[name='gamesubmit']"))

        mock.ui.input_text(form_name, game.name)
        if game.image_path is not None:
            form_image.send_keys(game.image_path)
        if game.publish:
            mock.ui.click(form_publish)
        url = env.URL_CREATE_GAME if fail else env.URL_CREATE_DM
        try:
            mock.check.submit_and_check(form_submit, url, partial_url=True)
            self.dm_games.append(game)
        except TimeoutException:
            if not fail:
                LOGGER.error(f'failing game: "{game}"')
            raise
        return game

    def edit_account(
        self,
        mock: Mock,
        name: str = None,
        email: str = None,
        password: str = None,
        different_confirm: str = None,
    ):
        self.edit_name(mock, name)
        self.edit_email(mock, email)
        self.edit_password(mock, password, different_confirm)

    def edit_name(self, mock: Mock, new: str):
        """navigate to account edit page and change name"""
        mock.ui.nav(env.URL_EDIT_ACCOUNT)
        if new is None:
            return
        LOGGER.debug(f"changing name to {new}")
        name = mock.ui.get_element(
            (By.CSS_SELECTOR, 'input[name="name-name"][type="text"]')
        )
        if not name.is_displayed():
            reveal_name = mock.ui.get_element((By.CSS_SELECTOR, 'a[data-edit="name"]'))
            mock.ui.click(reveal_name)
        mock.ui.input_text(name, new)
        submit = mock.ui.get_element(
            (By.CSS_SELECTOR, 'input[type="submit"][name="name-submit"]')
        )
        mock.ui.click(submit)
        # LOGGER.screencap(mock.ui.browser, "account_name")

    def edit_email(self, mock: Mock, new: str):
        """navigate to account edit page and change email"""
        mock.ui.nav(env.URL_EDIT_ACCOUNT)
        if new is None:
            return
        email = mock.ui.get_element(
            (By.CSS_SELECTOR, 'input[name="email-email"][type="text"]')
        )
        if not email.is_displayed():
            reveal_email = mock.ui.get_element(
                (By.CSS_SELECTOR, 'a[data-edit="email"]')
            )
            mock.ui.click(reveal_email)
        mock.ui.input_text(email, new)
        submit = mock.ui.get_element(
            (By.CSS_SELECTOR, 'input[type="submit"][name="email-submit"]')
        )
        mock.ui.click(submit)

    def edit_password(self, mock: Mock, new: str, confirm: str = None):
        """navigate to account edit page and change password"""
        mock.ui.nav(env.URL_EDIT_ACCOUNT)
        if new is None:
            return
        if confirm is None:
            confirm = new
        password = mock.ui.get_element(
            (By.CSS_SELECTOR, 'input[name="pass-password"][type="password"]')
        )
        if not password.is_displayed():
            reveal_password = mock.ui.get_element(
                (By.CSS_SELECTOR, 'a[data-edit="pass"]')
            )
            mock.ui.click(reveal_password)
        mock.ui.input_text(password, new)
        confirm_ = mock.ui.get_element(
            (By.CSS_SELECTOR, 'input[name="pass-confirm"][type="password"]')
        )
        mock.ui.input_text(confirm_, confirm)
        submit = mock.ui.get_element(
            (By.CSS_SELECTOR, 'input[type="submit"][name="pass-submit"]')
        )
        mock.ui.click(submit)

    def delete(self, mock: Mock, confirm_email: str = None, fail: bool = False):
        """navigate to account delete page and delete"""
        mock.ui.nav(env.URL_EDIT_ACCOUNT_DELETE)
        if confirm_email is None:
            confirm_email = self.email
        confirm = mock.ui.get_element(
            (By.CSS_SELECTOR, 'input[name="confirm"][type="text"]')
        )
        mock.ui.input_text(confirm, confirm_email)
        url = env.URL_EDIT_ACCOUNT_DELETE if fail else env.URL_AUTH_LOGIN
        submit = mock.ui.get_element((By.CSS_SELECTOR, 'input[type="submit"]'))
        mock.check.submit_and_check(submit, url)

    def new(
        self,
        name: str = None,
        email: str = None,
        password: str = None,
        different_confirm: str = None,
    ):
        self.id = next(env.ITERATOR)
        self.name = self.default_name(self.id) if name is None else name
        self.email = self.default_email(self.id) if email is None else email
        self.password = self.default_password(self.id) if password is None else password
        self.different_confirm = (
            self.password if different_confirm is None else different_confirm
        )

    def forced_to_reauth(self, mock: Mock):
        """force a stale session state and navigate the user to /edit/account which will force a re-authorization"""
        url = "/edit/account"
        mock.ui.make_session_stale()
        mock.ui.nav("/profile/account")
        account_link = mock.ui.get_element((By.CSS_SELECTOR, f"a[href='{url}']"))
        redirect_url = "/reauth" + query_string_convert(next="/edit/account")
        mock.check.submit_and_check(account_link, destination=redirect_url)
        return url

    def register_and_login(self, mock: Mock):
        self.auth_register(mock)
        self.auth_login(mock)

    def auth_register(self, mock: Mock, fail: bool = False):
        """
        registers the Mock user.
        :param fail: set to `True` if the registration will fail. Defaults to False
        """
        LOGGER.debug(f"registering: {self}")
        mock.ui.nav(env.URL_AUTH_REGISTER)
        form_name = mock.ui.get_element((By.CSS_SELECTOR, "input[name='name']"))
        form_email = mock.ui.get_element((By.CSS_SELECTOR, "input[name='email']"))
        form_password = mock.ui.get_element((By.CSS_SELECTOR, "input[name='password']"))
        form_confirm = mock.ui.get_element((By.CSS_SELECTOR, "input[name='confirm']"))

        mock.ui.input_text(form_name, self.name)
        mock.ui.input_text(form_email, self.email)
        mock.ui.input_text(form_password, self.password)
        mock.ui.input_text(form_confirm, self.different_confirm)

        form_submit = mock.ui.get_element((By.ID, "usersubmit"))
        url_after_submit = env.URL_AUTH_REGISTER if fail else env.URL_AUTH_LOGIN
        mock.check.submit_and_check(form_submit, url_after_submit)

    def auth_login(self, mock: Mock, remember: bool = True, fail: bool = False):
        """
        logs in the registered mock user.
        :param remember: If True, the login form will have a checkbox to "remember me", defaults to True
        """

        mock.ui.nav(env.URL_AUTH_LOGIN)

        form_email = mock.ui.get_element((By.CSS_SELECTOR, "input[name='email']"))
        form_password = mock.ui.get_element((By.CSS_SELECTOR, "input[name='password']"))
        form_submit = mock.ui.get_element((By.CSS_SELECTOR, "input[name='submit']"))
        remember_me = mock.ui.get_element((By.CSS_SELECTOR, "input[name='remember']"))

        if remember:
            mock.ui.click(remember_me)

        mock.ui.input_text(form_email, self.email)
        mock.ui.input_text(form_password, self.password)

        url_after_submit = env.URL_AUTH_LOGIN if fail else env.URL_INDEX
        mock.check.submit_and_check(form_submit, url_after_submit)

    def auth_reauth(self, mock: Mock, url: str):
        """re-authenticates the user.

        :param url: the subdomain expected to redirected from
        """
        form_email = mock.ui.get_element((By.CSS_SELECTOR, "input[name='email']"))
        form_password = mock.ui.get_element((By.CSS_SELECTOR, "input[name='password']"))
        form_submit = mock.ui.get_element((By.CSS_SELECTOR, "input[name='submit']"))
        mock.ui.input_text(form_email, self.email)
        mock.ui.input_text(form_password, self.password)
        mock.check.submit_and_check(form_submit, url)

    def auth_logout(self, mock: Mock):
        """Logout the user by navigating to the logout page"""
        mock.ui.nav(env.URL_AUTH_LOGOUT)

    def reset(self):
        self._set_attrs(reset=True)

    def _set_attrs(self, reset=False):
        self.id = next(env.ITERATOR)
        if self.name is None or reset:
            self.name = self.default_name(self.id)
        if self.email is None or reset:
            self.email = self.default_email(self.id)
        if self.password is None or reset:
            self.password = self.default_password(self.id)
        if self.different_confirm is None or reset:
            self.different_confirm = self.password