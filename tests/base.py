from flask_testing import TestCase

from project import app, db
from project.helpers import init_training_wheels_db
from project.classes import *


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'not secret'

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        db.create_all()
        #this adds the admin/tutorial account to the db
        init_training_wheels_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
