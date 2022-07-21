import imp
import pytest

from testing import ExpectedException
from testing.end_to_end import Mock


@pytest.mark.xfail
def test_can_edit_personal_notesTODO(mock: Mock):
    with mock.test_manager(test_can_edit_personal_notesTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_edit_player_notesTODO(mock: Mock):
    with mock.test_manager(test_can_edit_player_notesTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_edit_todm_notesTODO(mock: Mock):
    with mock.test_manager(test_can_edit_todm_notesTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_make_note_draftTODO(mock: Mock):
    with mock.test_manager(test_can_make_note_draftTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_cannot_make_note_todm_TODO(mock: Mock):
    with mock.test_manager(test_cannot_make_note_todm_TODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_publish_draftTODO(mock: Mock):
    with mock.test_manager(test_can_publish_draftTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_change_session_nameTODO(mock: Mock):
    with mock.test_manager(test_can_change_session_nameTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_change_session_numberTODO(mock: Mock):
    with mock.test_manager(test_can_change_session_numberTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_cannot_give_session_negative_numberTODO(mock: Mock):
    with mock.test_manager(test_cannot_give_session_negative_numberTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_cannot_edit_sessions_to_have_duplicate_numbersTODO(mock: Mock):
    with mock.test_manager(test_cannot_edit_sessions_to_have_duplicate_numbersTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_notes_made_by_characters_attached_to_deleted_accounts_can_be_editted_by_dmTODO(
    mock: Mock,
):
    with mock.test_manager(
        test_notes_made_by_characters_attached_to_deleted_accounts_can_be_editted_by_dmTODO
    ):
        raise ExpectedException()
