from selenium.webdriver.common.by import By

from end_to_end.helpers import redirect
from end_to_end.mock import Mock
import env

def test_join_redirects_anon_user(mock: Mock):
    with mock.test_manager(test_join_redirects_anon_user):
        mock.check.ui.nav(env.URL_JOIN)
        mock.check.confirm_url(redirect(env.URL_JOIN, env.URL_AUTH_LOGIN))

def test_join_assets(mock: Mock):
    with mock.test_manager(test_join_assets):
        mock.user.register_and_login(mock)
        game = mock.user.create_game_and_dm(mock)
        mock.user.auth_logout(mock)
        mock.add_user()
        mock.user.register_and_login(mock)
        mock.ui.nav(env.URL_JOIN)
        mock.check.nav_is_authenticated()
        header = mock.ui.get_element((By.CSS_SELECTOR, 'div.app-container h1'))
        assert header.text == "Public Games"
        game_links = mock.ui.get_all_elements((By.CSS_SELECTOR, 'div.game a'))
        assert game.name in [link.text for link in game_links]
