import os

from werkzeug.security import generate_password_hash
import flask_migrate

def Chronicler_db_init(db):
    """Progrmatically create the db and add the admin/Tutorial"""
    flask_migrate.upgrade()
    add_admin_to_db(db)

def config(app):
    """Set app.configs"""
    db_password = os.environ.get('DB_PASS')
    # Heroku
    if os.environ.get("HEROKU_HOSTING"):
        print("connecting to heroku...")
        app.config['SQLALCHEMY_DATABASE_URI'] = postfix(os.environ.get('DATABASE_URL'))
    # local
    elif os.environ.get("DOCKER_FLAG"):
        print("connecting to local through docker...")
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:" + db_password + "@chronicler_host:5432/chronicler_db"
    else:
        print("connecting to local...")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///litechronicler.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = db_password
    app.config['POSTGRES_PASSWORD'] = db_password
    app.config['SQLALCHEMY_ECHO'] = False

def create_postgres_connection(db_password):
    """create postgres database"""
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    # Connect to PostgreSQL DBMS

    con = psycopg2.connect(f"host='chronicler_host' user='postgres' password='{db_password}'")
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Obtain a DB Cursor
    cursor = con.cursor()
    name_Database = "chronicler_db"

    # Create table statement

    cursor.execute(f"DROP DATABASE IF EXISTS {name_Database};")
    sqlCreateDatabase = "create database "+name_Database+";"
    cursor.execute(sqlCreateDatabase)
    print(f"{name_Database} created")
    return

def add_admin_to_db(db):
    """add 'chronicler helper' to db as admin account."""
    from .classes import Users
    admin_pass = os.environ.get("ADMIN_PASS")
    chronicler_user = Users(name = "Chronicler", email="app@chronicler.gg", hashed_password=generate_password_hash(admin_pass, method='sha256'))
    db.session.add(chronicler_user)
    db.session.commit()

def ready_db(db, db_password):
    """Sets up db
    
    uses 'try' condition to test if the db has been initiated yet (is this the app's first run or not)
    if it is the first run the .get_admin() will traceback so it will move on to the except which initialized the db
    """
    try:
        from .classes import Users
        Users.get_admin()
        flask_migrate.upgrade()
    except:
        create_postgres_connection(db_password)
        Chronicler_db_init(db)


def postfix(string):
    if string is None:
        return None
    else:
        if string[0:9] == 'postgres:':
            new = 'postgresql' + string[8:]
            return new
        else:
            return string