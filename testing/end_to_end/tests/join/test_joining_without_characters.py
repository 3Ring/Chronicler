from testing.end_to_end import Mock
from testing.end_to_end.models import Characters
from testing.end_to_end.tests.join.join_helpers import joining_primer


def test_can_create_and_add_character(mock: Mock):
    with mock.test_manager(test_can_create_and_add_character):
        game = joining_primer(mock)
        character = Characters(mock.user)
        mock.user.join_game_with_create(mock, game, character)


def test_bad_character_names(mock: Mock):
    with mock.test_manager(test_bad_character_names):
        game = joining_primer(mock)
        mock.user.join_game_page(mock, game)
        character = Characters(mock.user)
        for bad_name in [
            "",
            " ",
            "       ",
            "B" * 51,
            "test" + "!@#$%^&*()-=./,'\"",
        ]:
            character.name = bad_name
            mock.user.join_game_with_create(
                mock, game, character, from_joining=True, fail=True
            )
