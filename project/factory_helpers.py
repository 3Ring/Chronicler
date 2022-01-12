import os

from werkzeug.security import generate_password_hash
from sqlalchemy_utils.functions import database_exists
import flask_migrate


def config_db_uri(app):
    db_password = os.environ.get("DB_PASS")
    # Heroku
    if os.environ.get("HEROKU_HOSTING"):
        print("connecting to heroku...")
        uri = postfix(os.environ.get("DATABASE_URL"))
    # local
    elif os.environ.get("DOCKER_FLAG"):
        print("connecting to local through docker...")
        uri = f"postgresql://postgres:{db_password}@chronicler_host:5432/chronicler_db"
    else:
        print("connecting to local...")
        uri = "sqlite:///litechronicler.db"

    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    if not database_exists(uri):
        print("creating database..")
        create_db()
        config_db_uri(app)
    return


def config(app):
    """Set app.configs"""
    db_password = os.environ.get("DB_PASS")
    config_db_uri(app)

    # SQLAlchemy
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = db_password
    app.config["POSTGRES_PASSWORD"] = db_password
    app.config["SQLALCHEMY_ECHO"] = False

    # Flask admin
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    return


def ready_db(app, test_config):
    """Sets up db with Flask Migrate"""
    # from .classes import Users
    if test_config is not None:
        app.config.update(test_config)
        return
    with app.app_context():

        try:
            flask_migrate.upgrade()
            print("success upgrade")
        except Exception as e:
            raise RuntimeError(
                """Flask Migrations/versions directory either not found or empty.\n 
                check your Migrations directory errors"""
            )
    return


def create_db():
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    db_password = os.environ.get("DB_PASS")
    con = psycopg2.connect(
        f"host='chronicler_host' user='postgres' password='{db_password}'"
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Obtain a DB Cursor
    cursor = con.cursor()
    name_Database = "chronicler_db"

    cursor.execute(f"DROP DATABASE IF EXISTS {name_Database};")
    sqlCreateDatabase = "create database " + name_Database + ";"
    cursor.execute(sqlCreateDatabase)
    print(f"{name_Database} created")
    return


def postfix(string):
    if string is None:
        return None
    else:
        if string[0:9] == "postgres:":
            new = "postgresql" + string[8:]
            return new
        else:
            return string
