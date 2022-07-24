from selenium.webdriver.common.by import By

from testing import globals as env
from testing.end_to_end import Mock
from testing.end_to_end.models import Games
from testing.end_to_end.helpers import images_path
from testing.end_to_end.tests.asset_helpers import (
    asset_validator_by_tag,
    asset_validator_by_css,
    asset_validator_by_id,
)

def test_create_game_page_assets(mock: Mock):
    with mock.test_manager(test_create_game_page_assets):
        mock.user.register_and_login(mock)
        mock.ui.nav(env.URL_CREATE_GAME)
        mock.ui.nav_is_authenticated()
        asset_validator_by_id(mock, "csrf_token", hidden=True)
        asset_validator_by_tag(mock, "form")
        asset_validator_by_tag(mock, "h1", text_to_check="Create your game!")
        asset_validator_by_tag(mock, "label", text_to_check="Name of your game")
        asset_validator_by_tag(mock, "label", text_to_check="(Optional) Game Image")
        asset_validator_by_tag(mock, "label", text_to_check="Publish? (Allow game to be searchable)")
        asset_validator_by_css(mock, "input[type='text']")
        asset_validator_by_css(mock, "input[type='file']")
        asset_validator_by_css(mock, "input[type='checkbox']")
        asset_validator_by_css(mock, "input[type='submit'")


def test_bad_game_names(mock: Mock):
    with mock.test_manager(test_bad_game_names):
        mock.user.register_and_login(mock)
        bad_names = [
            "",
            " ",
            "                 ",
            "test" * (60 // 4),
        ]
        for name in bad_names:
            game = Games(name=name)
            mock.user.create_game(mock, game=game, fail=True)
            mock.ui.browser.refresh()

def test_bad_game_images(mock: Mock):
    with mock.test_manager(test_bad_game_images):
        mock.user.register_and_login(mock)
        for fail in images_path(fail=True):
            game = Games(image_path=fail)
            mock.user.create_game(mock, game=game, fail=True)
            mock.ui.browser.refresh()

def test_user_can_create_game(mock: Mock):
    with mock.test_manager(test_user_can_create_game):
        mock.user.register_and_login(mock)
        mock.user.create_game(mock)


def test_game_is_displayed_when_published(mock: Mock):
    with mock.test_manager(test_game_is_displayed_when_published):
        mock.user.register_and_login(mock)
        game = mock.user.create_game_and_dm(mock, game_name="is_displayed_when_published")
        mock.add_user()
        mock.user.register_and_login(mock)
        mock.ui.nav(env.URL_JOIN)
        game_links = mock.ui.get_all_elements((By.CSS_SELECTOR, "div.games a"))
        assert True in [(link.text.find(game.name) != -1) for link in game_links]

def test_game_is_hidden_when_not_published(mock: Mock):
    with mock.test_manager(test_game_is_hidden_when_not_published):
        mock.user.register_and_login(mock)
        game = mock.user.create_game_and_dm(
            mock, game_name="not_displayed_when_unpublished", publish=False
        )
        mock.add_user()
        mock.user.register_and_login(mock)
        mock.user.create_game_and_dm(mock)
        mock.add_user()
        mock.user.register_and_login(mock)
        mock.ui.nav(env.URL_JOIN)
        game_links = mock.ui.get_all_elements((By.CSS_SELECTOR, "div.games a"))
        for link in game_links:
            assert link.text.find(game.name) == -1
