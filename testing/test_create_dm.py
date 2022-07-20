from selenium.webdriver.common.by import By

from end_to_end.mock import Mock
from end_to_end.helpers import images_path
from end_to_end.models import DMs, Games 


def test_create_dm_page_assets(mock: Mock):
    with mock.test_manager(test_create_dm_page_assets):
        mock.user.register_and_login(mock)
        game = mock.user.create_game(mock)
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
