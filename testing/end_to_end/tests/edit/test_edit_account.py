from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from testing.end_to_end.helpers import redirect
from testing.end_to_end import Mock
from testing import globals as env
from testing.end_to_end.tests.asset_helpers import (
    asset_validator_by_tag,
    asset_validator_by_css,
    asset_validator_by_id,
)

def check_hidden(mock: Mock, button: WebElement, elements: List[WebElement], start_hidden: bool = True):
    """checks that the element toggles between hidden and visible"""
    for boolean in [start_hidden, not start_hidden]:
        for element in elements:
            assert not element.is_displayed() if boolean else element.is_displayed()
        mock.ui.click(button)
        for element in elements:
            assert element.is_displayed() if boolean else not element.is_displayed()


def test_edit_account_assets(mock: Mock):
    with mock.test_manager(test_edit_account_assets):
        mock.user.register_and_login(mock)
        mock.ui.nav(env.URL_EDIT_ACCOUNT)
        mock.ui.nav_is_authenticated()

        # Top edit Menu
        asset_validator_by_tag(mock, "h1", text_to_check="Change Account info:")

        # change name form
        name_edit_button = asset_validator_by_tag(mock, "a[data-edit='name']", text_to_check="edit")
        mock.ui.click(name_edit_button)
        asset_validator_by_tag(mock, "label", text_to_check=f"Name: {mock.user.name}")
        asset_validator_by_id(mock, "name-csrf_token", hidden=True)
        name_form = [asset_validator_by_tag(mock, "label", text_to_check="Change Name")]
        name_name = asset_validator_by_css(mock, "input[name='name-name'][type='text']")
        assert name_name.get_attribute("value") == mock.user.name
        name_form.append(name_name)
        name_form.append(asset_validator_by_css(mock, "input[name='name-submit'][type='submit']"))
        check_hidden(mock, name_edit_button, name_form, start_hidden=False)

        # change email form
        email_edit_button = asset_validator_by_css(mock, "a[data-edit='email']", text_to_check="edit")
        mock.ui.click(email_edit_button)
        asset_validator_by_tag(mock, "label", text_to_check=f"Email: {mock.user.email}")
        asset_validator_by_id(mock, "email-csrf_token", hidden=True)
        email_form = [asset_validator_by_tag(mock, "label", text_to_check="Change Email")]
        email_email = asset_validator_by_css(mock, "input[name='email-email'][type='email']")
        assert email_email.get_attribute("value") == mock.user.email
        email_form.append(email_email)
        email_form.append(asset_validator_by_css(mock, "input[name='email-submit'][type='submit']"))
        check_hidden(mock, email_edit_button, email_form, start_hidden=False)

        # change password form
        password_edit_button = asset_validator_by_tag(mock, "a", text_to_check="Change Password")
        mock.ui.click(password_edit_button)
        asset_validator_by_id(mock, "pass-csrf_token", hidden=True)
        password_form = [
        asset_validator_by_css(mock, "label.form-label", text_to_check="Change Password"),
        asset_validator_by_tag(mock, "label", text_to_check="Show Passwords"),
        asset_validator_by_tag(mock, "label", text_to_check="Confirm New Password"),
        asset_validator_by_css(mock, "input[type='password'][name='pass-password']"),
        asset_validator_by_css(mock, "input[type='password'][name='pass-confirm']"),
        asset_validator_by_css(mock, "input[type='checkbox'][name='pass-reveal']"),
        ]
        check_hidden(mock, password_edit_button, password_form, start_hidden=False)

        # delete account form
        asset_validator_by_id(mock, "del-csrf_token", hidden=True)
        asset_validator_by_tag(mock, "h3", text_to_check="Delete Account:")
        asset_validator_by_tag(mock, "p", text_to_check="This will take you to another page to confirm and delegate assets")
        asset_validator_by_css(mock, "input[name='del-submit'][type='submit']")


def test_show_passwords_button_works(mock: Mock):
    with mock.test_manager(test_show_passwords_button_works):
        mock.user.register_and_login(mock)
        mock.ui.nav(env.URL_EDIT_ACCOUNT)
        password_edit_button = asset_validator_by_tag(mock, "a", text_to_check="Change Password")
        mock.ui.click(password_edit_button)
        password = asset_validator_by_css(mock, "input[type='password'][name='pass-password']")
        confirm = asset_validator_by_css(mock, "input[type='password'][name='pass-confirm']")
        reveal = asset_validator_by_css(mock, "input[type='checkbox'][name='pass-reveal']")
        mock.ui.click(reveal)
        assert password.get_attribute("type") == "text"
        assert confirm.get_attribute("type") == "text"


def test_edit_account_redirects_anon_user(mock: Mock):
    with mock.test_manager(test_edit_account_redirects_anon_user):
        mock.ui.nav(env.URL_EDIT_ACCOUNT)
        redirected = redirect(env.URL_EDIT_ACCOUNT, env.URL_AUTH_LOGIN)
        mock.ui.confirm_url(redirected)


def test_edit_account_name(mock: Mock):
    with mock.test_manager(test_edit_account_name):
        mock.user.register_and_login(mock)
        mock.user.name = f"changed_{mock.user.id}"
        mock.user.edit_name(mock, mock.user.name)
        mock.ui.nav(env.URL_PROFILE_ACCOUNT)
        asset_validator_by_tag(mock, "label", text_to_check=f"Name: {mock.user.name}")


def test_edit_account_email(mock: Mock):
    with mock.test_manager(test_edit_account_email):
        mock.user.register_and_login(mock)
        mock.user.email = f"changed{mock.user.id}@gmail.com"
        mock.user.edit_email(mock, mock.user.email)
        mock.ui.nav(env.URL_PROFILE_ACCOUNT)
        labels = mock.ui.get_all_elements((By.TAG_NAME, "label"))
        assert f"Email: {mock.user.email}" in [label.text for label in labels]
        mock.user.auth_logout(mock)
        mock.user.auth_login(mock)


def test_edit_account_password(mock: Mock):
    with mock.test_manager(test_edit_account_password):
        mock.user.register_and_login(mock)
        new_pass = f"Changed_{mock.user.id}"
        mock.user.change_password(new_pass)
        mock.user.edit_password(mock, mock.user.password)
        assert mock.user.password == new_pass
        mock.user.auth_logout(mock)
        mock.user.auth_login(mock)


def test_edit_account_delete(mock: Mock):
    with mock.test_manager(test_edit_account_delete):
        mock.user.register_and_login(mock)
        mock.user.delete(mock)
        mock.user.auth_login(mock, fail=True)
