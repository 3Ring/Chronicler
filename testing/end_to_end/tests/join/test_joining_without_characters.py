import pytest

from testing import ExpectedException
from testing.end_to_end import Mock


@pytest.mark.xfail
def test_joining_assetsTODO(mock: Mock):
    with mock.test_manager(test_joining_assetsTODO):
        raise ExpectedException()


@pytest.mark.xfail
def test_can_create_and_add_character(mock: Mock):
    with mock.test_manager(test_can_create_and_add_character):
        raise ExpectedException()


@pytest.mark.xfail
def test_bad_character_names(mock: Mock):
    with mock.test_manager(test_bad_character_names):
        raise ExpectedException()
