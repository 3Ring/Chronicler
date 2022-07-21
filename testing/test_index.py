from selenium.webdriver.common.by import By

from testing.end_to_end.mock import Mock
from testing.end_to_end.helpers import redirect
from testing import globals as env


def test_index_redirects_anon_user_to_login(mock: Mock):
    with mock.test_manager(test_index_redirects_anon_user_to_login):
        mock.ui.nav(env.URL_INDEX)
        mock.check.confirm_url(redirect(env.URL_INDEX, env.URL_AUTH_LOGIN))


def test_index_page_assets(mock: Mock):
    with mock.test_manager(test_index_page_assets):
        mock.user.register_and_login(mock)
        mock.check.confirm_url(env.URL_INDEX)
        mock.check.nav_is_authenticated()
        mock.ui.get_element(
            (By.CSS_SELECTOR, f'div.games a[href="{env.URL_CREATE_GAME}"]')
        )
        mock.ui.get_element((By.CSS_SELECTOR, f'div.games a[href="{env.URL_JOIN}"]'))
