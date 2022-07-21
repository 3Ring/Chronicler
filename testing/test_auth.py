from selenium.webdriver.common.by import By

from testing.end_to_end.helpers import redirect
from testing.end_to_end.mock import Mock
from testing import globals as env

def test_register_assets(mock: Mock):
    with mock.test_manager(test_register_assets):
        mock.ui.nav(env.URL_AUTH_REGISTER)
        mock.check.nav_is_anon(),
        mock.ui.get_element((By.CSS_SELECTOR, "input[name='name']"))
        mock.ui.get_element((By.CSS_SELECTOR, "input[name='email']"))
        mock.ui.get_element((By.CSS_SELECTOR, "input[name='password']"))
        mock.ui.get_element((By.CSS_SELECTOR, "input[name='confirm']"))
        mock.ui.get_element((By.CSS_SELECTOR, "input[name='reveal']"))
        mock.ui.get_element((By.CSS_SELECTOR, "input[name='usersubmit']"))


def test_show_passwords(mock: Mock):
    with mock.test_manager(test_show_passwords):
        mock.ui.nav(env.URL_AUTH_REGISTER)
        password = mock.ui.get_element((By.CSS_SELECTOR, "input[name='password']"))
        confirm = mock.ui.get_element((By.CSS_SELECTOR, "input[name='confirm']"))
        reveal = mock.ui.get_element((By.CSS_SELECTOR, "input[name='reveal']"))
    
        mock.ui.input_text(password, "password")
        mock.ui.input_text(confirm, "confirm")

        hidden_pw = mock.ui.get_element((By.CSS_SELECTOR, "input[name='password']"))
        assert hidden_pw.get_attribute("type") == "password"
        mock.ui.click(reveal)
        revealed_pw = mock.ui.get_element((By.CSS_SELECTOR, "input[name='password']"))
        assert revealed_pw.get_attribute("type") == "text"
        revealed_confirm = mock.ui.get_element(
            (By.CSS_SELECTOR, "input[name='confirm']")
        )
        assert revealed_confirm.get_attribute("type") == "text"


def test_register_link_to_login(mock: Mock):
    with mock.test_manager(test_register_link_to_login):
        mock.ui.nav(env.URL_AUTH_REGISTER)
        link = mock.ui.get_element((By.CSS_SELECTOR, f"form a[href='{env.URL_AUTH_LOGIN}']"))
        assert link.text == "Sign-in!"
        mock.check.click_link_and_confirm(link, env.URL_AUTH_LOGIN)


def test_login_link_to_register(mock: Mock):
    with mock.test_manager(test_login_link_to_register):
        mock.ui.nav(env.URL_AUTH_LOGIN)
        link = mock.ui.get_element((By.CSS_SELECTOR, f"a[href='{env.URL_AUTH_REGISTER}']"))
        mock.check.click_link_and_confirm(link, env.URL_AUTH_REGISTER)


def test_anonymous_user_redirected_to_login(mock: Mock):
    with mock.test_manager(test_anonymous_user_redirected_to_login):
        for url in [env.URL_AUTH_LOGOUT, env.URL_AUTH_REAUTH]:
            mock.ui.nav(url)
            redirected = redirect(url, env.URL_AUTH_LOGIN)
            mock.check.confirm_url(redirected)


def test_register_bad_user_names(mock: Mock):
    with mock.test_manager(test_register_bad_user_names):
        bad_names = [
            "",
            " ",
            "       ",
            "B",
            ("test" * 5) + "t",
            "test" + "!@#$%^&*()-=./,'\"",
        ]
        for name in bad_names:
            mock.user.name = name
            mock.user.auth_register(mock, fail=True)


def test_register_bad_emails(mock: Mock):
    with mock.test_manager(test_register_bad_emails):
        pass
        # TODO impliment email validation
        # for email in [
        #     "@gmail.com",
        #     "test",
        #     "       @gmail.com",
        #     ("test" * (120 // 3)) + "@gmail.com",
        #     "t@p.c",
        # ]:
        #     mock.user["email"] = email
        #     mock.auth.register(fail=True)


def test_register_bad_passwords(mock: Mock):
    with mock.test_manager(test_register_bad_passwords):
        bad_passwords = [
            ("", ""),
            ("         ", "         "),
            ("a", "a"),
            ("testtes", "testtes"),
            ("test" * (100 // 3), "test" * (100 // 3)),
            ("testtest", "testtest1"),
        ]
        for pw, confirm in bad_passwords:
            mock.user.password, mock.user.different_confirm = pw, confirm
#             mock.auth.register(fail=True)


def test_can_register(mock: Mock):
    with mock.test_manager(test_can_register):
        mock.user.auth_register(mock)


def test_register_does_not_login_user(mock: Mock):
    with mock.test_manager(test_register_does_not_login_user):
        mock.user.auth_register(mock)
        mock.check.nav_is_anon()


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
        mock.check.confirm_url(env.URL_INDEX)

def test_fresh_user_is_redirected_to_index_from_reauth(mock: Mock):
    with mock.test_manager(test_fresh_user_is_redirected_to_index_from_reauth):
        mock.user.register_and_login(mock)
        mock.ui.nav(env.URL_AUTH_REAUTH)
        mock.check.confirm_url(env.URL_INDEX)


def test_login_remember_me(mock: Mock):
    with mock.test_manager(test_login_remember_me):
        mock.user.register_and_login(mock)
        mock.ui.make_session_stale()
        mock.ui.nav(env.URL_AUTH_LOGIN)
        mock.check.confirm_url(env.URL_INDEX)


def test_user_can_reauth(mock: Mock):
    with mock.test_manager(test_user_can_reauth):
        mock.user.register_and_login(mock)
        url = mock.user.forced_to_reauth(mock)
        mock.user.auth_reauth(mock, url)


def test_can_logout(mock: Mock):
    with mock.test_manager(test_can_logout):
        mock.user.register_and_login(mock)
        mock.user.auth_logout(mock)
        mock.user.auth_login(mock)
