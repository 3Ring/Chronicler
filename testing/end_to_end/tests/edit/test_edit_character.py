import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from testing.end_to_end.helpers import redirect, images_path
from testing import ExpectedException
from testing import globals as env
from testing.end_to_end import Mock
from testing.end_to_end import exceptions as ex
from testing.end_to_end.models import Characters
from testing.end_to_end.tests.asset_helpers import (
    assets_validator_by_tag,
    asset_validator_by_tag,
    asset_validator_by_css,
    asset_validator_by_id,
)


def test_edit_character_assets(mock: Mock):
    with mock.test_manager(test_edit_character_assets):
        for image in images_path():
            img_path = image
            break
        character = Characters(
            mock.user, name="CharEditAssets", bio="CharEditBio", image_path=img_path
        )
        character = _character_creation(mock, character=character)
        url = character.get_edit_url(mock)
        mock.ui.nav(url)
        asset_validator_by_id(mock, "a-csrf_token", hidden=True)
        assets_validator_by_tag(mock, 2, "form")
        assets_validator_by_tag(mock, 2, "h1", character.name)
        asset_validator_by_tag(mock, "label", text_to_check="Name")
        name = asset_validator_by_css(mock, "input[name='a-name'][type='text']")
        assert name.get_attribute("value") == character.name
        # TODO character image validation
        # asset_validator_by_tag(mock, "img")
        asset_validator_by_tag(
            mock, "label", text_to_check="(Optional) Character Image"
        )
        asset_validator_by_css(mock, "input[type='file'][name='a-img']")
        asset_validator_by_tag(mock, "label", text_to_check="Bio")
        bio = asset_validator_by_css(mock, "textarea[name='a-bio']")
        assert bio.get_attribute("value") == character.bio
        asset_validator_by_css(mock, "input[name='a-submit'][type='submit']")


def test_edit_character_redirects_anon_user(mock: Mock):
    with mock.test_manager(test_edit_character_redirects_anon_user):
        character = _character_creation(mock)
        url = character.get_edit_url(mock)
        mock.user.auth_logout(mock)
        mock.ui.nav(url)
        current = redirect(url, env.URL_AUTH_LOGIN)
        mock.ui.confirm_url(current)


def test_different_user_cannot_access_char_edit(mock: Mock):
    with mock.test_manager(test_different_user_cannot_access_char_edit):
        character = _character_creation(mock)
        url = character.get_edit_url(mock)
        mock.add_user()
        mock.user.register_and_login(mock)
        mock.ui.nav(url)
        mock.ui.redirected(url, env.URL_INDEX)


def test_can_edit_name(mock: Mock):
    with mock.test_manager(test_can_edit_name):
        character = _character_creation(mock)
        new_name = "A New Name III"
        character.edit(mock, name=new_name)
        mock.ui.nav(env.URL_PROFILE_CHARACTERS)
        h2s = mock.ui.get_all_elements((By.TAG_NAME, "h2"))
        assert 0 in [el.text.find(new_name) for el in h2s]


def test_can_edit_image(mock: Mock):
    with mock.test_manager(test_can_edit_image):
        character = _character_creation(mock)
        mock.ui.nav(env.URL_PROFILE_CHARACTERS)
        old_image = _get_image(mock, character.name)
        assert old_image == _get_image(mock, character.name)
        new_path = os.path.abspath("test_images\pass\\1280x720.jpg")
        character.edit(mock, image_path=new_path)
        mock.ui.nav(env.URL_PROFILE_CHARACTERS)
        assert _get_image(mock, character.name) != old_image


def test_can_edit_bio(mock: Mock):
    with mock.test_manager(test_can_edit_bio):
        character = _character_creation(mock)
        new_bio = "once there was a story all about how my life got flipped turned up upsidedown"
        character.edit(mock, bio=new_bio)
        mock.ui.nav(env.URL_PROFILE_CHARACTERS)
        Ps = mock.ui.get_all_elements((By.TAG_NAME, "p"))
        assert 0 in [el.text.find(new_bio) for el in Ps]


@pytest.mark.xfail
def test_removing_character_removes_them_from_all_games(mock: Mock):
    with mock.test_manager(test_removing_character_removes_them_from_all_games):
        try:
            mock.user.register_and_login(mock)
            game1 = mock.user.create_game_and_dm(mock)
            game2 = mock.user.create_game_and_dm(mock)
            mock.add_user()
            mock.user.register_and_login(mock)
            game1_chars = mock.user.create_characters(mock, amount=3)
            game2_chars = [game1_chars[-1]]
            game2_chars.extend(mock.user.create_characters(mock, amount=2))
            mock.user.join_game_with_characters(mock, game1, game1_chars)
            mock.user.join_game_with_characters(mock, game2, game2_chars)
            for game in [game1, game2]:
                for i in range(1, len(game.characters)):
                    game.characters[i].get_edit_url(mock)
                    game.characters[i].leave_game(mock)
        except Exception:
            raise ExpectedException()


def _character_creation(mock: Mock, character: Characters = None) -> Characters:
    mock.user.register_and_login(mock)
    return mock.user.create_character(mock, character)


def _get_image(mock: Mock, name: str) -> str:
    char_divs = mock.ui.get_all_elements((By.CSS_SELECTOR, ".character"))
    for div in char_divs:
        name_header: WebElement = div.find_element(by=By.TAG_NAME, value="h2")
        if name_header.text.find(name) != -1:
            img: WebElement = div.find_element(by=By.TAG_NAME, value="img")
            return img.get_attribute("src")
    raise ex.CharacterMissingError(name, char_divs)
