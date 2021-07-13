from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from settings import db
import os


def postfix(string):
        if string[0:9] == 'postgres:':
                new = 'postgresql' + string[8:]
                return new
        else:
                return string

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db_password = os.environ.get('DB_PASS')
    app.config['SECRET_KEY'] = db_password or 'so-secret-I-have-no-idea-what-it-is'
    # PostGres config:
    app.config['SQLALCHEMY_DATABASE_URI'] = postfix(os.environ.get('DATABASE_URL')) or 'mysql+pymysql://root:' + db_password + '@localhost/BON'

    migrate = Migrate(app, db)

    # SQLite address
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///liteBON.db'

    from classes import Users

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app) 

    # provide login_manager with a unicode user ID
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from BONapp import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app