from testing.end_to_end import Mock


def test_can_logout(mock: Mock):
    with mock.test_manager(test_can_logout):
        mock.user.register_and_login(mock)
        mock.user.auth_logout(mock)
        mock.user.auth_login(mock)
