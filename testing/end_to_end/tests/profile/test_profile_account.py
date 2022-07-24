from selenium.webdriver.common.by import By

from testing.end_to_end.helpers import redirect
from testing.end_to_end import Mock
from testing import globals as env
from testing.end_to_end.tests.asset_helpers import (
    asset_validator_by_tag,
)

def test_profile_account_assets(mock: Mock):
    with mock.test_manager(test_profile_account_assets):
        mock.user.register_and_login(mock)
        mock.ui.nav(env.URL_PROFILE_ACCOUNT)
        asset_validator_by_tag(mock, "form")
        asset_validator_by_tag(mock, "h1", text_to_check="Account Details:")
        asset_validator_by_tag(mock, "label", text_to_check=f"Name: {mock.user.name}")
        asset_validator_by_tag(mock, "label", text_to_check=f"Email: {mock.user.email}")
        asset_validator_by_tag(mock, "a", text_to_check="Edit/delete account")