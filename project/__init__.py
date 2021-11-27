import os

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask import Flask

from project.factory_helpers import config, ready_db
from project.blueprints import init_blueprints
db_password = os.environ.get('DB_PASS')

db = SQLAlchemy()
migrate_ = Migrate()
socketio = SocketIO(cors_allowed_origins = '*')
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    """provide login_manager with a unicode user ID"""
    from project.models import Users
    return Users.query.get(int(user_id))

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__)
    config(app)
    db.init_app(app)
    migrate_.init_app(app, db, compare_type=True)
    ready_db(app, test_config)
    socketio.init_app(app)
    login_manager.init_app(app) 
    init_blueprints(app)

    # register events file with application
    from project import events
    
    # create db admins and orphanages
    from project.base_items import Base_items
    Base_items.init_database_assets(app)
    return app