import os

from werkzeug.security import generate_password_hash
import flask_migrate

# def Chronicler_db_init(db):
#     """Progrmatically create the db and add the admin/Tutorial"""
#     flask_migrate.upgrade()
#     add_admin_to_db(db)

def clean_slate(db_password):
    """deletes database. insert this function into create_app() to use"""
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    
    con = psycopg2.connect(f"host='chronicler_host' user='postgres' password='{db_password}'")
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    name_Database = "chronicler_db"
    con.cursor().execute(f"DROP DATABASE IF EXISTS {name_Database};")
    con.close()

def show_db_columns(db_password):

    import psycopg2
    con = psycopg2.connect(f"host='chronicler_host' user='postgres' password='{db_password}'")
    con.cursor().execute("SHOW DATABASES")
    for db in con:
        print(db)

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
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{db_password}@chronicler_host:5432/chronicler_db"
    else:
        print("connecting to local...")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///litechronicler.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = db_password
    app.config['POSTGRES_PASSWORD'] = db_password
    app.config['SQLALCHEMY_ECHO'] = False


def add_admin_to_db(db, Users):
    """add 'chronicler helper' to db as admin account."""

    admin_pass = os.environ.get("ADMIN_PASS")
    chronicler_user = Users(name = "Chronicler", email="app@chronicler.gg", hashed_password=generate_password_hash(admin_pass, method='sha256'))
    db.session.add(chronicler_user)
    db.session.commit()
    print(f"{chronicler_user.name} added to database..")

def ready_db(app):
    """Sets up db
    
    uses 'try' condition to test if the db has been initiated yet (is this the app's first run or not)
    if it is the first run the .get_admin() will traceback so it will move on to the except which initialized the db
    """
    db_not_initiated = False
    from .classes import Users
    with app.app_context():

        try:
            # _ = Users.get_admin()
            # print('2')
            flask_migrate.upgrade()
        except:
            print('3')
            db_not_initiated = True

    if db_not_initiated:
        return "not initiated"


def first_run(app, db, db_password):
    """creates database on host and initiates Flask Migrate"""
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    con = psycopg2.connect(f"host='chronicler_host' user='postgres' password='{db_password}'")
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Obtain a DB Cursor
    cursor = con.cursor()
    name_Database = "chronicler_db"

    cursor.execute(f"DROP DATABASE IF EXISTS {name_Database};")
    sqlCreateDatabase = "create database "+name_Database+";"
    cursor.execute(sqlCreateDatabase)
    print(f"{name_Database} created")

    from .classes import Users

    with app.app_context():
        try:
            print("initiating flask migrate..")
            flask_migrate.init()
            print("Migrating..")
            flask_migrate.migrate(message="initial migration")
            print("Upgrading..")
            flask_migrate.upgrade()
            print("adding admin to database..")
            add_admin_to_db(db, Users)
        except:
            raise RuntimeError(
                "Migration directory already exists. If you wish to reinitialize the Flask Migrate please delete Migrations folder"
                )


def postfix(string):
    if string is None:
        return None
    else:
        if string[0:9] == 'postgres:':
            new = 'postgresql' + string[8:]
            return new
        else:
            return string