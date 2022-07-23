import pytest

from testing.end_to_end.helpers import redirect
from testing import ExpectedException
from testing.end_to_end import Mock
from testing import globals as env





@pytest.mark.xfail
def test_can_create_new_character_and_add_to_gameTODO(mock: Mock):
    with mock.test_manager(test_can_create_new_character_and_add_to_gameTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_all_characters_are_listedTODO(mock: Mock):
    with mock.test_manager(test_all_characters_are_listedTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_add_multiple_characters(mock: Mock):
    with mock.test_manager(test_can_add_multiple_characters):
        raise ExpectedException()
