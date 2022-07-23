from testing.end_to_end import Mock

def joining_primer(mock: Mock):
    """first steps of joining tests"""
    mock.user.register_and_login(mock)
    mock.user.create_game_and_dm(mock)
    game = mock.user.dm_games[0]
    mock.user.auth_logout(mock)
    mock.add_user()
    mock.user.register_and_login(mock)
    mock.user.join_game_page(mock, game)