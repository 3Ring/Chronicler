import pytest
import os
from flask_migrate import init, migrate, upgrade

from tests.helpers.unit import build


@pytest.fixture(scope="session")
def ut_app():
    """application"""
    from unit_test import test as chronicler

    assert chronicler.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
    assert chronicler.config["TESTING"] == True
    yield chronicler


@pytest.fixture(scope="session")
def ut_client(ut_app):
    """test client"""
    with ut_app.app_context(), ut_app.test_request_context():
        with ut_app.test_client() as testing_client:
            yield testing_client


@pytest.fixture(scope="session")
def ut_set_database(temp_dir, ut_app):
    """database setup."""
    init(directory=os.path.join(temp_dir, "migrations"))
    migrate(directory=os.path.join(temp_dir, "migrations"))
    upgrade(directory=os.path.join(temp_dir, "migrations"))
    build(ut_app)
    yield
