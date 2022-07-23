from testing.end_to_end.helpers import redirect
from testing.end_to_end import Mock

from testing.end_to_end.tests.join.join_helpers import joining_primer


def test_can_create_new_character_and_add_to_game(mock: Mock):
    with mock.test_manager(test_can_create_new_character_and_add_to_game):
        game = joining_primer(mock)
        character = mock.user.create_character(mock)
        mock.user.join_game_with_characters(mock, game, [character])
        assert character.character_in_game(mock, game)
        assert character.character_in_profile(mock)


def test_can_add_multiple_characters(mock: Mock):
    with mock.test_manager(test_can_add_multiple_characters):
        game = joining_primer(mock)
        characters = mock.user.create_characters(mock, 4)
        mock.user.join_game_with_characters(mock, game, characters)
        for character in characters:
            assert character.character_in_game(mock, game)
            assert character.character_in_profile(mock)
