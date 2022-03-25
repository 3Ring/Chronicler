import os
from sqlalchemy_utils.functions import database_exists
from flask_migrate import upgrade

def get_root(file):
    root = file
    head, tail = os.path.split(root)
    while tail != "":
        root = head
        head, tail = os.path.split(head)
        if tail == "chronicler":
            return root
    raise BaseException("directory doesn't exist")

def prep_db(app, create, file, testing=False):
    with app.app_context():
        if create and not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
            if testing:
                create_db(app, host="chronicler_host_test")
            else:
                create_db(app)
        from project.setup.db_init_create.base_items import Base_items
        upgrade(directory=os.path.join(os.path.dirname(file), "migrations"))
        Base_items.init_database_assets(app)




def create_db(app, host='chronicler_host', user='postgres', password=None):
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    db_password = os.environ.get("DB_PASS") if password is None else password
    con = psycopg2.connect(
        f"host='{host}' user={user} password='{db_password}'"
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = con.cursor()
    name_Database = "chronicler_db"

    cursor.execute(f"DROP DATABASE IF EXISTS {name_Database};")
    sqlCreateDatabase = "create database " + name_Database + ";"
    cursor.execute(sqlCreateDatabase)
    assert database_exists(app.config["SQLALCHEMY_DATABASE_URI"])
    print(f"{name_Database} created")


def postfix(string):
    if string is None:
        return None
    else:
        if string[0:9] == "postgres:":
            new = "postgresql" + string[8:]
            return new
        else:
            return string
