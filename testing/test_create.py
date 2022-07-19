import os

from selenium.webdriver.common.by import By

from end_to_end.mock import Mock
from end_to_end.helpers import redirect
from end_to_end.assets import Character
import env
from end_to_end.helpers import bad_images_path

# Game page
def test_create_game_page_assets(mock: Mock):
    with mock.test_manager(test_create_game_page_assets):
        mock.actions.register_and_login()
        mock.ui.nav(env.URL_CREATE_GAME)
        mock.check.nav_is_authenticated()
        mock.ui.get_element((By.ID, "csrf_token")),
        mock.ui.get_element((By.CSS_SELECTOR, "input[type='text']"))
        mock.ui.get_element((By.CSS_SELECTOR, "input[type='file']"))
        mock.ui.get_element((By.CSS_SELECTOR, "input[type='checkbox']"))
        mock.ui.get_element((By.CSS_SELECTOR, "input[type='submit'"))


def test_bad_game_names(mock: Mock):
    with mock.test_manager(test_bad_game_names):
        mock.actions.register_and_login()
        game = mock.create.game_object(save=False)
        bad_names = [
            "",
            " ",
            "                 ",
            "test" * (60 // 4),
        ]
        for name in bad_names:
            game.name = name
            mock.actions.create.game(game, fail=True)


def test_bad_game_images(mock: Mock):
    with mock.test_manager(test_bad_game_images):
        mock.actions.register_and_login()
        mock.ui.nav(env.URL_CREATE_GAME)
        path = os.path.abspath(os.path.join(os.environ.get("TEST_IMAGES_PATH"), "fail"))
        _, _, files = next(os.walk(path))
        bad_images = [os.path.abspath(os.path.join(path, file)) for file in files]
        game = mock.create.game_object(save=False)
        for fail in bad_images:
            game.image_path = fail
            mock.actions.create.game(game, fail=True)


def test_user_can_create_game(mock: Mock):
    with mock.test_manager(test_user_can_create_game):
        mock.actions.register_and_login()
        mock.create.game()


def test_create_dm_page_assets(mock: Mock):
    with mock.test_manager(test_create_dm_page_assets):
        mock.actions.register_and_login()
        game = mock.create.game_object(game_name="dm_page_assets")
        mock.create.game(game)
        mock.ui.get_element((By.CSS_SELECTOR, "input[type='file']"))
        mock.ui.get_element(
            (By.CSS_SELECTOR, "img[src='/static/images/default_dm.jpg']")
        )
        mock.ui.get_element((By.CSS_SELECTOR, "input[type='submit']"))

        headers = mock.ui.get_all_elements((By.TAG_NAME, "h1"))
        dm_name_input = mock.ui.get_element(
            (By.CSS_SELECTOR, "input[type='text'][name='name']")
        )

        found = False
        for header in headers:
            if header.text.find(game.name) != -1:
                found = True
        assert found
        assert dm_name_input.get_attribute("value") == "DM"


# DM
def test_user_can_create_dm(mock: Mock):
    with mock.test_manager(test_user_can_create_dm):
        mock.actions.register_and_login()
        mock.actions.create_game_and_dm()


def test_bad_dm_names(mock: Mock):
    with mock.test_manager(test_bad_dm_names):
        mock.actions.register_and_login()
        game = mock.actions.create.game()
        for bad_name in [
            "",
            "      ",
            "b" * 51,
        ]:
            game.dm.name = bad_name
            mock.create.dm(game.dm, fail=True)


def test_bad_dm_images(mock: Mock):
    with mock.test_manager(test_bad_dm_images):
        mock.actions.register_and_login()
        game = mock.create.game()
        for fail in bad_images_path():
            game.dm.image_path = fail
            mock.actions.create.dm(game.dm, fail=True)


# Game created
def test_game_is_displayed_when_published(mock: Mock):
    with mock.test_manager(test_game_is_displayed_when_published):
        mock.actions.register_and_login()
        game = mock.actions.create_game_and_dm(game_name="is_displayed_when_published")
        mock.reset()
        mock.actions.register_and_login()
        mock.ui.nav(env.URL_JOIN)
        game_links = mock.ui.get_all_elements((By.CSS_SELECTOR, "div.games a"))
        game_found = False
        for link in game_links:
            if link.text.find(game.name) != -1:
                game_found = True
                break
        assert game_found


def test_game_is_hidden_when_not_published(mock: Mock):
    with mock.test_manager(test_game_is_hidden_when_not_published):
        mock.actions.register_and_login()
        game = mock.actions.create_game_and_dm(
            game_name="not_displayed_when_unpublished", publish=False
        )
        mock.reset()
        mock.actions.register_and_login()
        mock.actions.create_game_and_dm()
        mock.reset()
        mock.actions.register_and_login()
        mock.ui.nav(env.URL_JOIN)
        game_links = mock.ui.get_all_elements((By.CSS_SELECTOR, "div.games a"))
        for link in game_links:
            assert link.text.find(game.name) == -1


# Character
def test_anon_user_is_redirected_from_create_character(mock: Mock):
    with mock.test_manager(test_anon_user_is_redirected_from_create_character):
        mock.ui.nav(env.URL_CREATE_CHARACTER)
        redirected_url = redirect(env.URL_CREATE_CHARACTER, env.URL_AUTH_LOGIN)
        mock.check.confirm_url(redirected_url)


def test_create_character_assets(mock: Mock):
    with mock.test_manager(test_create_character_assets):
        mock.actions.register_and_login()
        mock.ui.nav(env.URL_CREATE_CHARACTER)
        mock.check.nav_is_authenticated()
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
        mock.actions.register_and_login()
        mock.ui.nav(env.URL_CREATE_CHARACTER)
        character = Character(mock.user)
        for bad_name in [
            "",
            " ",
            "       ",
            "B" * 51,
            "test" + "!@#$%^&*()-=./,'\"",
        ]:
            character.name = bad_name
            mock.create.character(character, fail=True)


def test_bad_character_images(mock: Mock):
    with mock.test_manager(test_bad_character_images):
        mock.actions.register_and_login()
        mock.ui.nav(env.URL_CREATE_CHARACTER)
        character = Character(mock.user)
        for bad_image in bad_images_path():
            character.image_path = bad_image
            mock.create.character(character, fail=True)


def test_bad_character_bios(mock: Mock):
    with mock.test_manager(test_bad_character_bios):
        mock.actions.register_and_login()
        mock.ui.nav(env.URL_CREATE_CHARACTER)
        character = Character(mock.user)
        for bad_bio in [
            "B" * 5001,
        ]:
            character.bio = bad_bio
            mock.create.character(character, fail=True)


def test_user_can_create_character(mock: Mock):
    with mock.test_manager(test_user_can_create_character):
        mock.actions.register_and_login()
        mock.ui.nav(env.URL_CREATE_CHARACTER)
        mock.create.character(Character(mock.user))
