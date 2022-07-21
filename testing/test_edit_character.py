import os

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from testing import globals
from testing.end_to_end.mock import Mock
from testing.end_to_end.models.characters import Characters
from testing.end_to_end import exceptions as ex


def test_can_edit_name(mock: Mock):
    with mock.test_manager(test_can_edit_name):
        character = _character_creation(mock)
        new_name = "A New Name III"
        character.edit(mock, name=new_name)
        mock.ui.nav(globals.URL_PROFILE_CHARACTERS)
        h2s = mock.ui.get_all_elements((By.TAG_NAME, "h2"))
        assert 0 in [el.text.find(new_name) for el in h2s]


def test_can_edit_image(mock: Mock):
    with mock.test_manager(test_can_edit_image):
        character = _character_creation(mock)
        mock.ui.nav(globals.URL_PROFILE_CHARACTERS)
        old_image = _get_image(mock, character.name)
        assert old_image == _get_image(mock, character.name)
        new_path = os.path.abspath("test_images\pass\\1280x720.jpg")
        print(f"new_image: {new_path}")
        character.edit(mock, image_path=new_path)
        mock.ui.nav(globals.URL_PROFILE_CHARACTERS)
        assert _get_image(mock, character.name) != old_image


def test_can_edit_bio(mock: Mock):
    with mock.test_manager(test_can_edit_bio):
        character = _character_creation(mock)
        new_bio = "once there was a story all about how my life got flipped turned up upsidedown"
        character.edit(mock, bio=new_bio)
        mock.ui.nav(globals.URL_PROFILE_CHARACTERS)
        Ps = mock.ui.get_all_elements((By.TAG_NAME, "p"))
        assert 0 in [el.text.find(new_bio) for el in Ps]


def _character_creation(mock: Mock) -> Characters:
    mock.user.register_and_login(mock)
    return mock.user.create_character(mock)


def _get_image(mock: Mock, name: str) -> str:
    char_divs = mock.ui.get_all_elements((By.CSS_SELECTOR, ".character"))
    for div in char_divs:
        name_header: WebElement = div.find_element(by=By.TAG_NAME, value="h2")
        if name_header.text.find(name) != -1:
            img: WebElement = div.find_element(by=By.TAG_NAME, value="img")
            return img.get_attribute("src")
    raise ex.CharacterMissingError(name, char_divs)
