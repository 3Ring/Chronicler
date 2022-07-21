import pytest

from testing import ExpectedException
from testing.end_to_end import Mock


@pytest.mark.xfail
def test_anon_user_is_redirected_to_loginTODO(mock: Mock):
    with mock.test_manager(test_anon_user_is_redirected_to_loginTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_joining_assestsTODO(mock: Mock):
    with mock.test_manager(test_joining_assestsTODO):
        raise ExpectedException()


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
