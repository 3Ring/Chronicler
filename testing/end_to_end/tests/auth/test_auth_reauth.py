from testing.end_to_end import Mock
from testing import globals as env

def test_fresh_user_is_redirected_to_index_from_reauth(mock: Mock):
    with mock.test_manager(test_fresh_user_is_redirected_to_index_from_reauth):
        mock.user.register_and_login(mock)
        mock.ui.nav(env.URL_AUTH_REAUTH)
        mock.check.confirm_url(env.URL_INDEX)


def test_user_can_reauth(mock: Mock):
    with mock.test_manager(test_user_can_reauth):
        mock.user.register_and_login(mock)
        url = mock.user.forced_to_reauth(mock)
        mock.user.auth_reauth(mock, url)