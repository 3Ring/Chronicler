from selenium.webdriver.common.by import By

from testing import globals as env
from testing.end_to_end import Mock
from testing.end_to_end.helpers import redirect, images_path
from testing.end_to_end.models import Characters
from testing.end_to_end.tests.asset_helpers import (
    asset_validator_by_css,
    asset_validator_by_tag,
    asset_validator_by_id,
)


def test_anon_user_is_redirected_from_create_character(mock: Mock):
    with mock.test_manager(test_anon_user_is_redirected_from_create_character):
        mock.ui.nav(env.URL_CREATE_CHARACTER)
        redirected_url = redirect(env.URL_CREATE_CHARACTER, env.URL_AUTH_LOGIN)
        mock.ui.confirm_url(redirected_url)


def test_create_character_assets(mock: Mock):
    with mock.test_manager(test_create_character_assets):
        mock.user.register_and_login(mock)
        mock.ui.nav(env.URL_CREATE_CHARACTER)
        mock.ui.nav_is_authenticated()
        asset_validator_by_id(mock, "csrf_token", hidden=True)
        asset_validator_by_tag(mock, "form")
        asset_validator_by_tag(mock, 'form h1', text_to_check='Create Character!')
        asset_validator_by_tag(mock, "label", text_to_check="(Optional) Character Image")
        asset_validator_by_tag(mock, "label", text_to_check="Bio")
        asset_validator_by_css(mock, "input[name='name'][type='text']")
        asset_validator_by_css(mock, "input[name='img'][type='file']")
        asset_validator_by_css(mock, "textarea[name='bio']")
        asset_validator_by_css(mock, "input[type='submit']")



def test_bad_character_names(mock: Mock):
    with mock.test_manager(test_bad_character_names):
        mock.user.register_and_login(mock)
        mock.ui.nav(env.URL_CREATE_CHARACTER)
        character = Characters(mock.user)
        for bad_name in [
            "",
            " ",
            "       ",
            "B" * 51,
            "test" + "!@#$%^&*()-=./,'\"",
        ]:
            character.name = bad_name
            mock.user.create_character(mock, character, fail=True)


def test_bad_character_images(mock: Mock):
    with mock.test_manager(test_bad_character_images):
        mock.user.register_and_login(mock)
        mock.ui.nav(env.URL_CREATE_CHARACTER)
        character = Characters(mock.user)
        for bad_image in images_path(fail=True):
            character.image_path = bad_image
            mock.user.create_character(mock, character, fail=True)


def test_bad_character_bios(mock: Mock):
    with mock.test_manager(test_bad_character_bios):
        mock.user.register_and_login(mock)
        mock.ui.nav(env.URL_CREATE_CHARACTER)
        character = Characters(mock.user)
        for bad_bio in [
            "B" * 5001,
        ]:
            character.bio = bad_bio
            mock.user.create_character(mock, character, fail=True)


def test_user_can_create_character(mock: Mock):
    with mock.test_manager(test_user_can_create_character):
        mock.user.register_and_login(mock)
        mock.ui.nav(env.URL_CREATE_CHARACTER)
        mock.user.create_character(mock, Characters(mock.user))
