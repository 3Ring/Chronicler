import pytest

from testing import ExpectedException
from testing.end_to_end import Mock

@pytest.mark.xfail
def test_cannot_see_dm_only_notesTODO(mock: Mock):
    with mock.test_manager(test_cannot_see_dm_only_notesTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_cannot_see_draft_notesTODO(mock: Mock):
    with mock.test_manager(test_cannot_see_draft_notesTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_switch_view_to_different_sessionTODO(mock: Mock):
    with mock.test_manager(test_can_switch_view_to_different_sessionTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_switching_session_does_not_change_session_for_othersTODO(mock: Mock):
    with mock.test_manager(
        test_switching_session_does_not_change_session_for_othersTODO
    ):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_reorder_direction_of_notesTODO(mock: Mock):
    with mock.test_manager(test_can_reorder_direction_of_notesTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_reordering_direction_does_not_change_view_for_othersTODO(mock: Mock):
    with mock.test_manager(
        test_reordering_direction_does_not_change_view_for_othersTODO
    ):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_see_notes_added_to_new_session_by_othersTODO(mock: Mock):
    with mock.test_manager(test_can_see_notes_added_to_new_session_by_othersTODO):
        raise ExpectedException()

@pytest.mark.xfail
def test_adding_note_to_different_session_does_not_change_view_for_othersTODO(mock: Mock):
    with mock.test_manager(test_adding_note_to_different_session_does_not_change_view_for_othersTODO):
        raise ExpectedException()