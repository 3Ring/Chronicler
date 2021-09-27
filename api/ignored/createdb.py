import mysql.connector
import os
db_password = os.environ.get('DB_PASS')

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd = db_password,
)


my_cursor = mydb.cursor()

my_cursor.execute("DROP DATABASE IF EXISTS BON")
my_cursor.execute("CREATE DATABASE BON")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
my_cursor.close()

# The code above needs to be run to create the db of 'bon'.
# Then open a python shell in the directory that holds 'project' and enter these commands:
# "from project import db, create_app"
# "db.create_all(app=create_app())"
# this took me forever to figure out