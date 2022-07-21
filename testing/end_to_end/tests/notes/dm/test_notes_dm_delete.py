import pytest

from testing import ExpectedException
from testing.end_to_end import Mock


@pytest.mark.xfail
def test_can_delete_personal_notesTODO(mock: Mock):
    with mock.test_manager(test_can_delete_personal_notesTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_delete_other_notesTODO(mock: Mock):
    with mock.test_manager(test_can_delete_other_notesTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_others_see_deleted_notes_as_deleted_by_DMNameTODO(mock: Mock):
    with mock.test_manager(test_others_see_deleted_notes_as_deleted_by_DMNameTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_deleted_note_notification_disappears_on_refreshTODO(mock: Mock):
    with mock.test_manager(test_deleted_note_notification_disappears_on_refreshTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_delete_sessionTODO(mock: Mock):
    with mock.test_manager(test_can_delete_sessionTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_deleted_session_is_seen_as_deleted_by_DMNameTODO(mock: Mock):
    with mock.test_manager(test_deleted_session_is_seen_as_deleted_by_DMNameTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_cannot_delete_session_with_notesTODO(mock: Mock):
    with mock.test_manager(test_cannot_delete_session_with_notesTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_deleted_session_notification_disappears_on_refreshTODO(mock: Mock):
    with mock.test_manager(test_deleted_session_notification_disappears_on_refreshTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_notes_made_by_characters_attached_to_deleted_accounts_can_be_deleted_by_dmTODO(
    mock: Mock,
):
    with mock.test_manager(
        test_notes_made_by_characters_attached_to_deleted_accounts_can_be_deleted_by_dmTODO
    ):
        raise ExpectedException()
