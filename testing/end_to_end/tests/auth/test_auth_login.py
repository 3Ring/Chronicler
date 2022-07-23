from selenium.webdriver.common.by import By

from testing.end_to_end import Mock
from testing import globals as env
from testing.end_to_end.tests.asset_helpers import (
    assets_by_css_validator,
    assets_by_tag_validator,
)


def test_login_assets(mock: Mock):
    with mock.test_manager(test_login_assets):
        mock.ui.nav(env.URL_AUTH_LOGIN)
        mock.ui.nav_is_anon()
        assets_by_tag_validator(mock, 1, "h1", text_to_check="Log in")
        assets_by_tag_validator(mock, 1, "form")
        assets_by_tag_validator(mock, 1, "label", text_to_check="Email")
        assets_by_css_validator(mock, 1, "input[name='email'][type='text']")
        assets_by_tag_validator(mock, 1, "label", text_to_check="Password")
        assets_by_css_validator(mock, 1, "input[name='password'][type='password']")
        assets_by_tag_validator(mock, 1, "label", text_to_check="Remember Me")
        assets_by_css_validator(mock, 1, "input[name='remember'][type='checkbox']")
        assets_by_css_validator(mock, 1, "input[type='submit']")
        assets_by_tag_validator(mock, 1, "h6", text_to_check="Don't have an account?")
        assets_by_tag_validator(mock, 1, "a", text_to_check="Create One")


def test_login_link_to_register(mock: Mock):
    with mock.test_manager(test_login_link_to_register):
        mock.ui.nav(env.URL_AUTH_LOGIN)
        link = mock.ui.get_element(
            (By.CSS_SELECTOR, f"a[href='{env.URL_AUTH_REGISTER}']")
        )
        mock.ui.click_link_and_confirm(link, env.URL_AUTH_REGISTER)


def test_bad_logins(mock: Mock):
    with mock.test_manager(test_bad_logins):
        email: str
        pw: str
        email, pw = mock.user.email, mock.user.password
        mock.user.auth_register(mock)
        for email, password in [
            ("", ""),
            ("", pw),
            (email, ""),
            (email + "1", pw),
            (email, pw + "1"),
            (email.upper(), pw),
            (email, pw.upper()),
            (email.lower(), pw.lower()),
            (email.upper(), pw.upper()),
            (email.lower(), pw.upper()),
            (email.upper(), pw.lower()),
        ]:
            mock.user.email = email
            mock.user.password = password
            mock.user.auth_login(mock, fail=True)


def test_user_can_login(mock: Mock):
    with mock.test_manager(test_user_can_login):
        mock.user.register_and_login(mock)
        mock.ui.confirm_url(env.URL_INDEX)


def test_login_remember_me(mock: Mock):
    with mock.test_manager(test_login_remember_me):
        mock.user.register_and_login(mock)
        mock.ui.make_session_stale()
        mock.ui.nav(env.URL_AUTH_LOGIN)
        mock.ui.confirm_url(env.URL_INDEX)
