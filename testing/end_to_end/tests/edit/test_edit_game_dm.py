import pytest

from testing import ExpectedException
from testing.end_to_end import Mock


@pytest.mark.xfail
def test_edit_game_redirects_anon_userTODO(mock: Mock):
    with mock.test_manager(test_edit_game_redirects_anon_userTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_user_is_redirected_if_not_their_gameTODO(mock: Mock):
    with mock.test_manager(test_user_is_redirected_if_not_their_gameTODO):
        raise ExpectedException()


@pytest.mark.xfail
def edit_game_assetsTODO(mock: Mock):
    with mock.test_manager(edit_game_assetsTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_change_nameTODO(mock: Mock):
    with mock.test_manager(test_can_change_nameTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_change_imageTODO(mock: Mock):
    with mock.test_manager(test_can_change_imageTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_change_publishTODO(mock: Mock):
    with mock.test_manager(test_can_change_publishTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_bad_name_changesTODO(mock: Mock):
    with mock.test_manager(test_bad_name_changesTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_bad_image_changesTODO(mock: Mock):
    with mock.test_manager(test_bad_image_changesTODO):
        raise ExpectedException()
