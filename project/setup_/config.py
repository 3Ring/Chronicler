import os

from sqlalchemy_utils.functions import database_exists
db_password = os.environ.get("DB_PASS")

def config(app):
    """configure application and its libraries"""
    conf_sqla(app)
    conf_admin(app)

def conf_sqla(app):
    """configure SQLAlchemy"""
    uri = set_uri()
    if not database_exists(uri):
        print("No database found..", "\ncreating database...")
        from project.setup_.helpers import create_db
        create_db()


    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SECRET_KEY"] = db_password
    app.config["POSTGRES_PASSWORD"] = db_password
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

def set_uri():
    # Heroku
    if os.environ.get("HEROKU_HOSTING"):
        print("connecting to heroku...")
        uri = postfix(os.environ.get("DATABASE_URL"))
    # local
    elif os.environ.get("DOCKER_FLAG"):
        print("connecting to local through docker...")
        uri = f"postgresql://postgres:{db_password}@chronicler_host:5432/chronicler_db"
        # uri = f"postgresql://nbaiybhjzwkkpy:{db_password}@chronicler_host:5432/chronicler_db"
    else:
        print("connecting to local...")
        uri = "sqlite:///litechronicler.db"

    return uri

def postfix(string):
    """replaces depreciated 'postgres:' with 'postgresql'"""
    if string is None:
        return None
    else:
        if string[0:9] == "postgres:":
            new = "postgresql" + string[8:]
            return new
        else:
            return string

def conf_admin(app):
    """configure Flask Admin"""
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'