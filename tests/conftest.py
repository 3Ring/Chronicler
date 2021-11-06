import os
import tempfile

from flask import url_for
from werkzeug.utils import redirect
from project.__init__ import create_app, db
from flask_migrate import init, migrate, upgrade
import pytest

from project.factory_helpers import add_admin_to_db

admin_pass = os.environ.get("ADMIN_PASS")
def db_init_for_tests(db, path):
    """Progrmatically create the db and add the admin/Tutorial"""
    init(directory=path)
    migrate(directory=path)
    upgrade(directory=path)
    add_admin_to_db(db)

@pytest.fixture
def app(test_email=None):

    app = create_app({
        'TESTING': True
        ,'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:' 
        # ,'SQLALCHEMY_ECHO': True
    })

    with app.app_context():
        with tempfile.TemporaryDirectory() as tdp:
            db_init_for_tests(db, tdp)
        yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

class AuthActions:
    
    

    email_user = "register_test_email@chronicler.gg"
    email_admin = "app@chronicler.gg"
    password_user = "test123"
    name_user = "test_user"
    password_admin = admin_pass
    
    def __init__(self, client):
        self._client = client



    def login(self, model=None, email=email_user, password=password_user):
        if model != None:
            email = model.email
            password = model.hashed_password
        return self._client.post(
            url_for('auth.login'), data={"email": email, "password": password}, follow_redirects=True
        )
    
    def register(self, model, confirm=None):
        if confirm == None:
            confirm = model.hashed_password
        return self._client.post(
            "http://localhost/register", data={"name": model.name, "email": model.email, "password": model.hashed_password, "confirm": confirm}, follow_redirects=True
        )

    def logout(self):
        return self._client.get('/logout') 


@pytest.fixture
def auth(client):
    return AuthActions(client)