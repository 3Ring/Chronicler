from testing.end_to_end.helpers import redirect
from testing.end_to_end import Mock
from testing import globals as env


def test_anonymous_user_redirected_to_login(mock: Mock):
    with mock.test_manager(test_anonymous_user_redirected_to_login):
        for url in [env.URL_AUTH_LOGOUT, env.URL_AUTH_REAUTH]:
            mock.ui.nav(url)
            redirected = redirect(url, env.URL_AUTH_LOGIN)
            mock.check.confirm_url(redirected)
