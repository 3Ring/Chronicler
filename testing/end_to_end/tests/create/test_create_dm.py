from selenium.webdriver.common.by import By

from testing.end_to_end import Mock
from testing.end_to_end.helpers import images_path
from testing.end_to_end.models import DMs, Games 
from testing.end_to_end.tests.asset_helpers import (
    asset_validator_by_tag,
    asset_validator_by_css,
    asset_validator_by_id,
)


def test_create_dm_page_assets(mock: Mock):
    with mock.test_manager(test_create_dm_page_assets):
        mock.user.register_and_login(mock)
        game = mock.user.create_game(mock)
        mock.ui.nav_is_authenticated()
        asset_validator_by_id(mock, "csrf_token", hidden=True)
        asset_validator_by_tag(mock, "form")
        asset_validator_by_tag(mock, "h1", text_to_check='Personalize your "DM" avatar')
        asset_validator_by_tag(mock, "label", text_to_check='(Optional) Name different than default of "DM"')
        asset_validator_by_tag(mock, "label", text_to_check="(Optional) personalized DM Image")
        asset_validator_by_css(mock, "input[type='file']")
        asset_validator_by_css(mock, "img[src='/static/images/default_dm.jpg']")
        asset_validator_by_css(mock, "input[type='submit']")
        asset_validator_by_tag(mock, "h1", text_to_check=game.name)
        dm_name_input = asset_validator_by_css(mock, "input[type='text'][name='name']")
        assert dm_name_input.get_attribute("value") == "DM"


def test_user_can_create_dm(mock: Mock):
    with mock.test_manager(test_user_can_create_dm):
        mock.user.register_and_login(mock)
        mock.user.create_game_and_dm(mock)


def test_bad_dm_names(mock: Mock):
    with mock.test_manager(test_bad_dm_names):
        mock.user.register_and_login(mock)
        game: Games = mock.user.create_game(mock)
        for bad_name in [
            "",
            "      ",
            "b" * 51,
        ]:
            dm = DMs(user=mock.user, name=bad_name)
            mock.user.create_dm(mock, game, dm=dm, fail=True)
            mock.ui.browser.refresh()

def test_bad_dm_images(mock: Mock):
    with mock.test_manager(test_bad_dm_images):
        mock.user.register_and_login(mock)
        game: Games = mock.user.create_game(mock)
        for fail in images_path(fail=True):
            dm = DMs(user=mock.user, image_path=fail)
            mock.user.create_dm(mock, game, dm=dm, fail=True)
            mock.ui.browser.refresh()
