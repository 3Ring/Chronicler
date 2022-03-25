# -*- coding: utf-8 -*-
"""
    flaskbb.configs.default
    ~~~~~~~~~~~~~~~~~~~~~~~

    This is the default configuration for FlaskBB that every site should have.
    You can override these configuration variables in another class.

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
import os
import sys
import datetime
from dotenv import load_dotenv

from project.setup.helpers import postfix


class DefaultConfig(object):

    # Get the app root path
    #            <_basedir>
    # ../../ -->  chronicler/project/configs/base.py
    basedir = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    )

    # set environmental variables
    load_dotenv(".env")
    db_password = os.environ.get("DB_PASS")
    # Python version
    py_version = "{0.major}{0.minor}".format(sys.version_info)

    # Flask Settings
    # ------------------------------
    # There is a whole bunch of more settings available here:
    # http://flask.pocoo.org/docs/0.11/config/#builtin-configuration-values
    DEBUG = False
    TESTING = False

    # The preferred url scheme. In a productive environment it is highly
    # recommended to use 'https'.
    # This only affects the url generation with 'url_for'.
    # PREFERRED_URL_SCHEME = "https"

    # Allowed Hosts
    # A List of allowed hosts who will be considered "safe" when redirecting
    # urls. If set to None only the host currently serving this website
    # will be considered "safe".
    # ALLOWED_HOSTS = None

    # Database
    # ------------------------------
    # For PostgresSQL:
    # try:

    SQLALCHEMY_DATABASE_URI = postfix(os.environ.get("DATABASE_URL"))
    # except Exception:
    # SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:{db_password}@chronicler_host:5432/chronicler_db"
    # For SQLite:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir + '/' + \
    #                           'chronicler.sqlite'

    # just to supress warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # This will print all SQL statements
    SQLALCHEMY_ECHO = False

    # ALEMBIC = {
    #     "script_location": os.path.join(basedir, "/migrations"),
    #     "version_locations": "",
    #     "file_template": "%%(year)d%%(month).2d%%(day).2d%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s",
    # }
    # ALEMBIC_CONTEXT = {"render_as_batch": True}

    # Security
    # ------------------------------
    # This is the secret key that is used for session signing.
    # You can generate a secure key with os.urandom(24)
    SECRET_KEY = db_password

    # You can generate the WTF_CSRF_SECRET_KEY the same way as you have
    # generated the SECRET_KEY. If no WTF_CSRF_SECRET_KEY is provided, it will
    # use the SECRET_KEY.
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = db_password

    # The name of the cookie to store the “remember me” information in.
    REMEMBER_COOKIE_NAME = "remember_token"
    # The amount of time before the cookie expires, as a datetime.timedelta object.
    REMEMBER_COOKIE_DURATION = datetime.timedelta(days=365)
    # If the “Remember Me” cookie should cross domains,
    # set the domain value here (i.e. .example.com would allow the cookie
    # to be used on all subdomains of example.com).
    REMEMBER_COOKIE_DOMAIN = None
    # Limits the “Remember Me” cookie to a certain path.
    # REMEMBER_COOKIE_PATH = "/"
    # Restricts the “Remember Me” cookie’s scope to secure channels (typically HTTPS).
    REMEMBER_COOKIE_SECURE = None
    # Prevents the “Remember Me” cookie from being accessed by client-side scripts.
    # REMEMBER_COOKIE_HTTPONLY = True

    # Flask admin bootstrap theme
    FLASK_ADMIN_SWATCH = "cerulean"
