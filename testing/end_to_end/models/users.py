from __future__ import annotations
from typing import TYPE_CHECKING, List

from testing import exceptions as ex

if TYPE_CHECKING:
    from testing.end_to_end import Mock


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
    player_games: List[Games] = field(default_factory=list)
    dm_games: List[Games] = field(default_factory=list)
    characters: List[Characters] = field(default_factory=list)

    def __post_init__(self):
        self.id = next(env.ITERATOR)
        if self.name is None:
            self.name = self.default_name(self.id)
        if self.email is None:
            self.email = self.default_email(self.id)
        if self.password is None:
            self.password = self.default_password(self.id)
        if self.different_confirm is None:
            self.different_confirm = self.password

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
            mock.ui.submit_and_check(form_submit, url)
            self.player_games.append(character)
            return character
        except TimeoutException:
            if not fail:
                LOGGER.error(f'failing character: "{character}"')
            raise

    def create_characters(
        self, mock: Mock, amount: int = 1, characters: List[Characters] = []
    ) -> List[Characters]:
        """add multiple characters to mock and append them to self"""
        if characters:
            for character in characters:
                self.create_character(mock, character=character)
                self.characters.append(character)
        else:
            out = []
            for _ in range(amount):
                character = self.create_character(mock)
                out.append(character)
                self.characters.append(character)
            return out

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
            mock.ui.submit_and_check(form_submit, url, partial_url=True)
            game.dm = dm
            game.url = mock.ui.chronicler_url()
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
            mock.ui.submit_and_check(form_submit, url, partial_url=True)
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
        mock.ui.submit_and_check(submit, url)

    def forced_to_reauth(self, mock: Mock):
        """force a stale session state and navigate the user to /edit/account which will force a re-authorization"""
        url = "/edit/account"
        mock.ui.make_session_stale()
        mock.ui.nav("/profile/account")
        account_link = mock.ui.get_element((By.CSS_SELECTOR, f"a[href='{url}']"))
        redirect_url = "/reauth" + query_string_convert(next="/edit/account")
        mock.ui.submit_and_check(account_link, destination=redirect_url)
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
        mock.ui.submit_and_check(form_submit, url_after_submit)

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
        mock.ui.submit_and_check(form_submit, url_after_submit)

    def auth_reauth(self, mock: Mock, url: str):
        """re-authenticates the user.

        :param url: the subdomain expected to redirected from
        """
        form_email = mock.ui.get_element((By.CSS_SELECTOR, "input[name='email']"))
        form_password = mock.ui.get_element((By.CSS_SELECTOR, "input[name='password']"))
        form_submit = mock.ui.get_element((By.CSS_SELECTOR, "input[name='submit']"))
        mock.ui.input_text(form_email, self.email)
        mock.ui.input_text(form_password, self.password)
        mock.ui.submit_and_check(form_submit, url)

    def auth_logout(self, mock: Mock):
        """Logout the user by navigating to the logout page"""
        mock.ui.nav(env.URL_AUTH_LOGOUT)

    def join_game_page(self, mock: Mock, game: Games) -> None:
        mock.ui.nav(env.URL_JOIN)
        game_links = mock.ui.get_all_elements((By.CSS_SELECTOR, "div.games a"))
        for link in game_links:
            if link.text.find(game.name) != -1:

                mock.ui.click(link)
        confirms = mock.ui.get_all_elements((By.CSS_SELECTOR, "a.game_confirm"))
        for confirm in confirms:
            if (
                confirm.get_attribute("href").find(
                    f"game_name={game.name.replace(' ', '+')}"
                )
                != -1
            ):
                return mock.ui.click_link_and_confirm(
                    confirm, env.URL_JOINING_PRE, partial_url=True
                )
        raise ex.GameNotFoundError(
            f"game: {game.name} not found in elements href: {[el.get_attribute('href') for el in confirms]}"
        )

    def join_game_with_create(
        self, mock: Mock, game: Games, character: Characters = None
    ):
        self.join_game_page(mock, game)
        create_name = mock.ui.get_element(
            (By.CSS_SELECTOR, "input[name='create-name']")
        )
        mock.ui.input_text(create_name, character.name)
        if character is None:
            character = Characters(self)
        if character.bio is not None:
            create_bio = mock.ui.get_element(
                (By.CSS_SELECTOR, "textarea[name='create-bio']")
            )
            mock.ui.input_text(create_bio, character.bio)
        if character.image_path is not None:
            create_image = mock.ui.get_element(
                (By.CSS_SELECTOR, "input[name='create-img']")
            )
            create_image.send_keys(character.image_path)
        create_submit = mock.ui.get_element(
            (By.CSS_SELECTOR, "input[name='create-submit']")
        )
        mock.ui.click_link_and_confirm(create_submit, env.URL_NOTES, partial_url=True)
        game.characters.append(character)
        character.games.append(game)

    def join_game_with_characters(
        self,
        mock: Mock,
        game: Games,
        characters: List[Characters],
        add_to_game_object=True,
    ):
        """navigates to join page, adds characters, and submits form
        appends characters to game if not already there"""
        self.join_game_page(mock, game)
        labels = mock.ui.get_all_elements((By.TAG_NAME, "label"))
        for character in characters:
            for option in labels:
                if option.text.find(character.name) != -1:
                    mock.ui.click(option)
                    break
        add_submit = mock.ui.get_element((By.CSS_SELECTOR, "input[name='add-submit']"))
        mock.ui.click_link_and_confirm(add_submit, game.url)
        if not add_to_game_object:
            return
        for character in characters:
            if character not in game.characters:
                character.games.append(game)
                game.characters.append(character)

    def delete_attached(self, mock: Mock):
        for character in self.characters:
            character.delete(mock)
        for game in self.dm_games:
            game.delete(mock)
        self.characters.clear()
        self.dm_games.clear()
        self.player_games.clear()
