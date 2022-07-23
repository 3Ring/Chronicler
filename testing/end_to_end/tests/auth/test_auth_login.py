from selenium.webdriver.common.by import By

from testing.end_to_end import Mock
from testing import globals as env


def test_login_link_to_register(mock: Mock):
    with mock.test_manager(test_login_link_to_register):
        mock.ui.nav(env.URL_AUTH_LOGIN)
        link = mock.ui.get_element((By.CSS_SELECTOR, f"a[href='{env.URL_AUTH_REGISTER}']"))
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
