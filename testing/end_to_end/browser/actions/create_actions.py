from dataclasses import dataclass
from pyparsing import Char
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from _logging import Logger
from end_to_end.browser.ui import BrowserUI
from end_to_end.browser.actions.check_actions import CheckActions
from end_to_end.assets import Game, User, DM, Character
import env


@dataclass
class CreateActions:
    ui: BrowserUI
    logger: Logger
    user: User
    check: CheckActions

    def game_object(
        self,
        game_name: str = None,
        publish: bool = True,
        dm_image_path: str = None,
        dm_name: str = None,
        game_image_path: str = None,
        save: bool = True,
    ) -> Game:
        dm = DM(user=self.user, name=dm_name, image_path=dm_image_path)
        game = Game(
            dm=dm,
            publish=publish,
            name=game_name,
            image_path=game_image_path,
        )
        if save:
            self.user.dm_games.append(game)
        return game

    def game(self, game: Game = None, fail: bool = False) -> Game:
        if game is None:
            game = self.game_object(save=not fail)
        self.ui.nav(env.URL_CREATE_GAME)
        form_name = self.ui.get_element(
            (By.CSS_SELECTOR, "input[type='text'][name='name']")
        )
        form_image = self.ui.get_element((By.CSS_SELECTOR, "input[type='file']"))
        form_publish = self.ui.get_element((By.CSS_SELECTOR, "input[name='published']"))

        if game.publish:
            self.ui.click(form_publish)
        self.ui.input_text(form_name, game.name)
        if game.image_path is not None:
            form_image.send_keys(game.image_path)
        form_submit = self.ui.get_element((By.CSS_SELECTOR, "input[name='gamesubmit']"))
        url = env.URL_CREATE_GAME if fail else env.URL_CREATE_DM
        try:
            self.check.submit_and_check(form_submit, url, partial_url=True)
        except TimeoutException:
            if fail:
                self.logger.error(f'failing game: "{game}"')
            raise
        return game

    def dm(self, dm: DM, default_dm_name: bool = False, fail=False) -> None:
        """must be already on the correct page"""

        form_name = self.ui.get_element((By.CSS_SELECTOR, "input[type='text']"))
        form_image = self.ui.get_element(
            (By.CSS_SELECTOR, "input[name='img'][type='file']")
        )
        form_submit = self.ui.get_element((By.CSS_SELECTOR, "input[type='submit']"))

        if not default_dm_name:
            self.ui.input_text(form_name, dm.name)
        if dm.image_path:
            form_image.send_keys(dm.image_path)
        url = env.URL_CREATE_DM if fail else env.URL_NOTES
        try:
            self.check.submit_and_check(form_submit, url, partial_url=True)
        except TimeoutException:
            if fail:
                self.logger.error(f'failing dm: "{dm}"')
            raise

    def character(self, character: Character, success_url: str = env.URL_PROFILE_CHARACTERS, default_name: bool = False, fail: bool = False):

        self.ui.nav(env.URL_CREATE_CHARACTER)
        self.check.confirm_url(env.URL_CREATE_CHARACTER)

        form_name = self.ui.get_element(
            (By.CSS_SELECTOR, "input[name='name'][type='text']")
        )
        form_image = self.ui.get_element(
            (By.CSS_SELECTOR, "input[name='img'][type='file']")
        )
        form_bio = self.ui.get_element((By.CSS_SELECTOR, "textarea[name='bio']"))
        form_submit = self.ui.get_element((By.CSS_SELECTOR, "input[type='submit']"))

        if not default_name:
            self.ui.input_text(form_name, character.name)
        if character.image_path:
            form_image.send_keys(character.image_path)
        if character.bio:
            self.ui.input_text(form_bio, character.bio)
        url = env.URL_CREATE_CHARACTER if fail else success_url
        try:
            self.check.submit_and_check(form_submit, url)
        except TimeoutException:
            if fail:
                self.logger.error(f'failing character: "{character}"')
            raise
        return character



