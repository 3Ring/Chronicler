from selenium.webdriver.common.by import By

from end_to_end.helpers import redirect
from end_to_end.mock import Mock
import env


# def test_cannot_access_another_users_account(mock: Mock):
#     with mock.test_manager(test_cannot_access_another_users_account):
#         pass


def test_edit_account_name(mock: Mock):
    with mock.test_manager(test_edit_account_name):
        mock.actions.register_and_login()
        mock.user.name = f"changed_{mock.user.id}"
        mock.edit.account_name(mock.user.name)
        mock.ui.nav(env.URL_PROFILE_ACCOUNT)
        labels = mock.ui.get_all_elements((By.TAG_NAME, "label"))
        assert f"Name: {mock.user.name}" in [label.text for label in labels]


def test_edit_account_email(mock: Mock):
    with mock.test_manager(test_edit_account_email):
        mock.actions.register_and_login()
        mock.user.email = f"changed{mock.user.id}@gmail.com"
        mock.edit.account_email(mock.user.email)
        mock.ui.nav(env.URL_PROFILE_ACCOUNT)
        labels = mock.ui.get_all_elements((By.TAG_NAME, "label"))
        assert f"Email: {mock.user.email}" in [label.text for label in labels]
        mock.auth.logout()
        mock.auth.login()


def test_edit_account_password(mock: Mock):
    with mock.test_manager(test_edit_account_password):
        mock.actions.register_and_login()
        new_pass = f"Changed_{mock.user.id}"
        mock.user.change_password(new_pass)
        mock.edit.account_password(mock.user.password)
        assert mock.user.password == new_pass
        mock.auth.logout()
        mock.auth.login()


def test_edit_account_delete(mock: Mock):
    with mock.test_manager(test_edit_account_delete):
        mock.actions.register_and_login()
        mock.edit.account_delete()
        mock.auth.login(fail=True)

