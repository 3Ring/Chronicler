from testing.end_to_end import Mock
from testing.end_to_end.models import Games

def joining_primer(mock: Mock) -> Games:
    """first steps of joining tests
    creates game, logs out creator and registers/logs in new user.
    returns created game object
    """
    mock.user.register_and_login(mock)
    mock.user.create_game_and_dm(mock)
    game = mock.user.dm_games[0]
    mock.user.auth_logout(mock)
    mock.add_user()
    mock.user.register_and_login(mock)
    return game

