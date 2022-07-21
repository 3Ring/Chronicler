import pytest
from selenium.webdriver.common.by import By

from testing.end_to_end import Mock
from testing import globals as env
from testing import ExpectedException

@pytest.mark.xfail
def test_edit_account_redirects_anon_user(mock: Mock):
    with mock.test_manager(test_edit_account_redirects_anon_user):
        raise ExpectedException()


def test_edit_account_name(mock: Mock):
    with mock.test_manager(test_edit_account_name):
        mock.user.register_and_login(mock)
        mock.user.name = f"changed_{mock.user.id}"
        mock.user.edit_name(mock, mock.user.name)
        mock.ui.nav(env.URL_PROFILE_ACCOUNT)
        labels = mock.ui.get_all_elements((By.TAG_NAME, "label"))
        assert f"Name: {mock.user.name}" in [label.text for label in labels]


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
