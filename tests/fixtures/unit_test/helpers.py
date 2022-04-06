import pytest

from tests.helpers.unit import build, _reset_empty


@pytest.fixture()
def ut_reset_empty(ut_app):
    _reset_empty()
    yield True
    build(ut_app)


@pytest.fixture()
def ut_reset_before(ut_app):
    _reset_empty()
    build(ut_app)
    yield True


@pytest.fixture()
def ut_reset_after(ut_app):
    yield True
    _reset_empty()
    build(ut_app)
