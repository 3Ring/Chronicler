from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from testing.end_to_end import Mock
    from testing.end_to_end.models import Users, Games

from dataclasses import dataclass, field

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from testing import globals as env
import testing.end_to_end.exceptions as ex


@dataclass
class Characters:
    id: int = field(default=None, init=False)
    player: Users
    name: str = None
    bio: str = None
    image_path: str = None
    games: list[Games] = field(default_factory=list)

    def __post_init__(self):
        self.id = next(env.ITERATOR)
        if self.name is None:
            self.name = self.default_name(self.player.name, self.id)
        if self.bio is None:
            self.bio = self.default_bio(self.player.name, self.id)
        self.player.characters.append(self)

    @staticmethod
    def default_bio(name: str, id: int):
        return f"BIO {name} {id}"

    @staticmethod
    def default_name(name: str, id: int):
        return f"CHARACTER {name} {id}"

    def delete(self, mock: Mock, fail: bool = False, delete_self: bool = True):
        """deletes character from mock, then deletes object"""
        if fail or not delete_self:
            return
        del self

    def character_in_game(self, mock: Mock, game: Games) -> bool:
        """returns True if character is an option in the notes page"""
        mock.ui.nav(game.url, confirm=True)
        options = mock.ui.get_all_elements(
            (By.CSS_SELECTOR, "select[name='speaking_as'] option")
        )
        return True in [(o.text.find(self.name) != -1) for o in options]

    def character_in_profile(self, mock: Mock) -> bool:
        """returns True if character is listed in profile of logged in user"""
        mock.ui.nav(env.URL_PROFILE_CHARACTERS)
        headers = mock.ui.get_all_elements((By.TAG_NAME, "h2"))
        return True in [(h.text.find(self.name) != -1) for h in headers]

    def edit(self, mock: Mock, name: str = None, image_path=None, bio: str = None):
        if not any((name, image_path, bio)):
            return
        mock.ui.nav(env.URL_PROFILE_CHARACTERS)
        edit_links = mock.ui.get_all_elements((By.CSS_SELECTOR, "h2"))
        edit_anchor = self._get_edit_anchor_element(edit_links)
        mock.ui.click_link_and_confirm(
            edit_anchor, env.URL_EDIT_CHARACTERS_PRE, partial_url=True
        )

        if name is not None:
            form_name = mock.ui.get_element(
                (By.CSS_SELECTOR, f"input[value='{self.name}']")
            )
            self.name = name
            mock.ui.input_text(form_name, self.name)

        if image_path is not None:
            form_image = mock.ui.get_element((By.CSS_SELECTOR, "input[type='file']"))
            self.image_path = image_path
            form_image.send_keys(self.image_path)

        if bio is not None:
            form_bio = mock.ui.get_element((By.CSS_SELECTOR, "textarea[name='a-bio']"))
            self.bio = bio
            mock.ui.input_text(form_bio, self.bio)

        form_submit = mock.ui.get_element((By.CSS_SELECTOR, "input[type='submit']"))
        mock.ui.click_link_and_confirm(form_submit, env.URL_PROFILE_CHARACTERS)

    def _get_edit_anchor_element(self, elements: list[WebElement]) -> WebElement:
        """find and return characters webelement or raise exception if missing"""
        for el in elements:
            if el.text.find(self.name) != -1:
                return el.find_element(by=By.TAG_NAME, value="a")
        raise ex.CharacterMissingError(self.name, elements)
