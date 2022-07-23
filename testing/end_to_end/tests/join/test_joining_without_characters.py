import pytest

from testing import ExpectedException
from testing.end_to_end import Mock
from testing.end_to_end.tests.join.join_helpers import joining_primer



@pytest.mark.xfail
def test_can_create_and_add_character(mock: Mock):
    with mock.test_manager(test_can_create_and_add_character):
        raise ExpectedException()
        # game = joining_primer(mock)
        # mock.user.join_game_with_create(mock, game)


@pytest.mark.xfail
def test_bad_character_names(mock: Mock):
    with mock.test_manager(test_bad_character_names):
        raise ExpectedException()
