import pytest

from testing import ExpectedException
from testing.end_to_end import Mock


@pytest.mark.xfail
def test_session_logTODO(mock: Mock):
    with mock.test_manager(test_session_logTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_correct_portraitsTODO(mock: Mock):
    with mock.test_manager(test_correct_portraitsTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_speaking_asTODO(mock: Mock):
    with mock.test_manager(test_speaking_asTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_new_note_formTODO(mock: Mock):
    with mock.test_manager(test_new_note_formTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_session_cardTODO(mock: Mock):
    with mock.test_manager(test_session_cardTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_backgroundTODO(mock: Mock):
    with mock.test_manager(test_backgroundTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_game_nameTODO(mock: Mock):
    with mock.test_manager(test_game_nameTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_edit_or_delete_note_menuTODO(mock: Mock):
    with mock.test_manager(test_edit_or_delete_note_menuTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_edit_note_formTODO(mock: Mock):
    with mock.test_manager(test_edit_note_formTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_new_session_formTODO(mock: Mock):
    with mock.test_manager(test_new_session_formTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_edit_session_menuTODO(mock: Mock):
    with mock.test_manager(test_edit_session_menuTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_edit_session_formTODO(mock: Mock):
    with mock.test_manager(test_edit_session_formTODO):
        raise ExpectedException()
