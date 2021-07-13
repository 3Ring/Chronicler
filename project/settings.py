import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

db_password = os.environ.get('DB_PASS')

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = db_password or 'so-secret-I-have-no-idea-what-it-is'
app.config['SQLALCHEMY_DATABASE_URI'] = postfix(os.environ.get('DATABASE_URL')) or 'mysql+pymysql://root:' + db_password + '@localhost/BON'
db = SQLAlchemy(app)