import pytest

from testing import ExpectedException
from testing.end_to_end import Mock


@pytest.mark.xfail
def test_user_is_redirected_if_not_in_gameTODO(mock: Mock):
    with mock.test_manager(test_user_is_redirected_if_not_in_gameTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_add_characterTODO(mock: Mock):
    with mock.test_manager(test_can_add_characterTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_add_multiple_charactersTODO(mock: Mock):
    with mock.test_manager(test_can_add_multiple_charactersTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_characters_already_in_game_are_not_an_option_to_addTODO(mock: Mock):
    with mock.test_manager(
        test_characters_already_in_game_are_not_an_option_to_addTODO
    ):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_remove_characterTODO(mock: Mock):
    with mock.test_manager(test_can_remove_characterTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_remove_mulitple_charactersTODO(mock: Mock):
    with mock.test_manager(test_can_remove_mulitple_charactersTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_remove_all_characters_without_leaving_gameTODO(mock: Mock):
    with mock.test_manager(test_can_remove_all_characters_without_leaving_gameTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_leave_game(mock: Mock):
    with mock.test_manager(test_can_leave_game):
        raise ExpectedException()


@pytest.mark.xfail
def test_leaving_a_game_and_rejoining_requires_adding_characters_againTODO(mock: Mock):
    with mock.test_manager(
        test_leaving_a_game_and_rejoining_requires_adding_characters_againTODO
    ):
        raise ExpectedException()
