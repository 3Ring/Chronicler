from selenium.webdriver.common.by import By

from testing import globals as env
from testing.end_to_end import Mock
from testing.end_to_end.helpers import redirect, images_path
from testing.end_to_end.models import Characters


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
        mock.ui.get_element((By.TAG_NAME, "form"))
        headers = mock.ui.get_all_elements((By.CSS_SELECTOR, "form h1"))
        found = False
        for header in headers:
            if header.text.find("Create Character!") != -1:
                found = True
        assert found
        mock.ui.get_element((By.CSS_SELECTOR, "input[name='name'][type='text']"))
        mock.ui.get_element((By.CSS_SELECTOR, "input[name='img'][type='file']"))
        mock.ui.get_element((By.CSS_SELECTOR, "textarea[name='bio']"))
        mock.ui.get_element((By.CSS_SELECTOR, "input[type='submit']"))


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
