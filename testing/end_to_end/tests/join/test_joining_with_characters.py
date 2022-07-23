import pytest

from testing.end_to_end.helpers import redirect
from testing import ExpectedException
from testing.end_to_end import Mock
from testing import globals as env

from testing.end_to_end.tests.join.join_helpers import joining_primer


def test_can_create_new_character_and_add_to_game(mock: Mock):
    with mock.test_manager(test_can_create_new_character_and_add_to_game):
        game = joining_primer(mock)
        character = mock.user.create_character(mock)
        mock.user.join_game_with_characters(mock, game, [character])
        assert character.character_in_game(mock, game)
        assert character.character_in_profile(mock)


@pytest.mark.xfail
def test_all_characters_are_listedTODO(mock: Mock):
    with mock.test_manager(test_all_characters_are_listedTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_add_multiple_characters(mock: Mock):
    with mock.test_manager(test_can_add_multiple_characters):
        raise ExpectedException()


@pytest.mark.xfail
def test_characters_already_in_game_are_not_an_optionTODO(mock: Mock):
    with mock.test_manager(test_characters_already_in_game_are_not_an_optionTODO):
        raise ExpectedException()
