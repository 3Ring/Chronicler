import os

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask import Flask

from .factory_helpers import config, ready_db, first_run, add_admin_to_db


db = SQLAlchemy()
migrate_ = Migrate()

socketio = SocketIO(cors_allowed_origins = '*')
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
db_password = os.environ.get('DB_PASS')

@login_manager.user_loader
def load_user(user_id):
    """provide login_manager with a unicode user ID"""

    from project.models import Users
    return Users.query.get(int(user_id))


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    from project.models import Users
    app = Flask(__name__)
    config(app)
    db.init_app(app)
    migrate_.init_app(app, db)
    if test_config is not None:
        app.config.update(test_config)
    else:
        readied = ready_db(app)
        if readied == "not initiated" and not os.environ.get("HEROKU_HOSTING"):
            first_run(app, db, db_password)
            add_admin_to_db(app, Users)
    socketio.init_app(app)
    login_manager.init_app(app) 
    
    # blueprint for auth routes of app
    from project.views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from project.views.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # register events file with application
    from project import events
    return app