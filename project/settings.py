import os
from flask import Flask
# this function is here because heroku returns "postgres://.." which is depreciated and not accepted by sqlalchemy. it should be 'postgresql://...'
def postfix(string):
    if string is None:
        return None
    else:
        if string[0:9] == 'postgres:':
            new = 'postgresql' + string[8:]
            return new
        else:
            return string

app = Flask(__name__)

db_password = os.environ.get('DB_PASS')
# Heroku
if os.environ.get("HEROKU_HOSTING"):
    print("connecting to heroku...")
    app.config['SQLALCHEMY_DATABASE_URI'] = postfix(os.environ.get('DATABASE_URL'))
# local
elif os.environ.get("DOCKER_FLAG"):
    print("connecting to local through docker...")
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:" + db_password + "@bonsqldb:5432/bon"
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:' + db_password + '@bonmysqldb:3306/BON'
else:
    print("connecting to local...")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:' + db_password + '@localhost/BON'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = db_password
app.config['POSTGRES_PASSWORD'] = db_password
app.config['SQLALCHEMY_ECHO'] = False




