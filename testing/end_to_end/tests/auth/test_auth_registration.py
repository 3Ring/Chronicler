import pytest
from selenium.webdriver.common.by import By

from testing import ExpectedException
from testing.end_to_end import Mock
from testing import globals as env
from testing.end_to_end.tests.asset_helpers import (
    asset_validator_by_tag,
    asset_validator_by_css,
)

def test_register_assets(mock: Mock):
    with mock.test_manager(test_register_assets):
        mock.ui.nav(env.URL_AUTH_REGISTER)
        mock.ui.nav_is_anon(),
        asset_validator_by_css(mock, "input[name='name']")
        asset_validator_by_css(mock, "input[name='name']")
        asset_validator_by_css(mock, "input[name='email']")
        asset_validator_by_css(mock, "input[name='password']")
        asset_validator_by_css(mock, "input[name='confirm']")
        asset_validator_by_css(mock, "input[name='reveal']")
        asset_validator_by_css(mock, "input[name='usersubmit']")


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
        link = mock.ui.get_element(
            (By.CSS_SELECTOR, f"form a[href='{env.URL_AUTH_LOGIN}']")
        )
        assert link.text == "Sign-in!"
        mock.ui.click_link_and_confirm(link, env.URL_AUTH_LOGIN)


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

@pytest.mark.xfail
def test_register_bad_emails_TODO(mock: Mock):
    with mock.test_manager(test_register_bad_emails_TODO):
        raise ExpectedException()
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
            mock.user.auth_register(mock, fail=True)


def test_can_register(mock: Mock):
    with mock.test_manager(test_can_register):
        mock.user.auth_register(mock)


def test_register_does_not_login_user(mock: Mock):
    with mock.test_manager(test_register_does_not_login_user):
        mock.user.auth_register(mock)
        mock.ui.nav_is_anon()
