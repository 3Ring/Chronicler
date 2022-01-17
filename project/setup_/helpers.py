import os
import flask_migrate



def update_db(app, test_config):
    """Sets up db with Flask Migrate"""

    if test_config is not None:
        app.config.update(test_config)
        return
    with app.app_context():
            flask_migrate.upgrade()



def create_db():
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    db_password = os.environ.get("DB_PASS")
    con = psycopg2.connect(
        f"host='chronicler_host' user='postgres' password='{db_password}'"
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

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
