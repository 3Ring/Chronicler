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
def test_can_create_todm_noteTODO(mock: Mock):
    with mock.test_manager(test_can_create_todm_noteTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_add_note_to_new_session_without_refreshTODO(mock: Mock):
    with mock.test_manager(test_can_add_note_to_new_session_without_refreshTODO):
        raise ExpectedException()
