import pytest

from testing import ExpectedException
from testing.end_to_end import Mock


@pytest.mark.xfail
def test_can_edit_personal_notesTODO(mock: Mock):
    with mock.test_manager(test_can_edit_personal_notesTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_cannot_edit_player_notesTODO(mock: Mock):
    with mock.test_manager(test_cannot_edit_player_notesTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_edit_todm_notesTODO(mock: Mock):
    with mock.test_manager(test_can_edit_todm_notesTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_edit_draft_notesTODO(mock: Mock):
    with mock.test_manager(test_can_edit_draft_notesTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_make_note_draftTODO(mock: Mock):
    with mock.test_manager(test_can_make_note_draftTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_others_cannot_see_new_draft_without_refreshTODO(mock: Mock):
    with mock.test_manager(test_others_cannot_see_new_draft_without_refreshTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_make_note_todm_TODO(mock: Mock):
    with mock.test_manager(test_can_make_note_todm_TODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_publish_draftTODO(mock: Mock):
    with mock.test_manager(test_can_publish_draftTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_edit_notes_of_owned_removed_charactersTODO(mock: Mock):
    with mock.test_manager(test_can_edit_notes_of_owned_removed_charactersTODO):
        raise ExpectedException()
