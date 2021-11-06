import os

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask import Flask

from .factory_helpers import config, ready_db, clean_slate, show_db_columns, first_run


db = SQLAlchemy()
migrate_ = Migrate()
socketio = SocketIO()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
db_password = os.environ.get('DB_PASS')

@login_manager.user_loader
def load_user(user_id):
    """provide login_manager with a unicode user ID"""
    from .classes import Users
    return Users.query.get(int(user_id))


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__)
    config(app)
    db.init_app(app)
    migrate_.init_app(app, db)
    # clean_slate(db_password)
    if test_config is not None:
        app.config.update(test_config)
    else:
        readied = ready_db(app)
        if readied == "not initiated":
            first_run(app, db, db_password)
    socketio.init_app(app)
    login_manager.init_app(app) 

    # blueprint for auth routes of app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .BONapp import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app