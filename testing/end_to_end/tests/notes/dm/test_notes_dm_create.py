import imp
import pytest

from testing import ExpectedException
from testing.end_to_end import Mock


@pytest.mark.xfail
def test_can_create_new_noteTODO(mock: Mock):
    with mock.test_manager(test_can_create_new_noteTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_create_draftTODO(mock: Mock):
    with mock.test_manager(test_can_create_draftTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_cannot_create_todm_noteTODO(mock: Mock):
    with mock.test_manager(test_cannot_create_todm_noteTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_create_new_session(mock: Mock):
    with mock.test_manager(test_can_create_new_session):
        raise ExpectedException()


@pytest.mark.xfail
def test_cannot_create_session_with_negative_numberTODO(mock: Mock):
    with mock.test_manager(test_cannot_create_session_with_negative_numberTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_cannot_create_session_with_duplicate_numberTODO(mock: Mock):
    with mock.test_manager(test_cannot_create_session_with_duplicate_numberTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_new_session_is_placed_in_correct_orderTODO(mock: Mock):
    with mock.test_manager(test_new_session_is_placed_in_correct_orderTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_all_users_can_see_new_session_without_refreshTODO(mock: Mock):
    with mock.test_manager(test_all_users_can_see_new_session_without_refreshTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_add_note_to_new_session_without_refreshTODO(mock: Mock):
    with mock.test_manager(test_can_add_note_to_new_session_without_refreshTODO):
        raise ExpectedException()
