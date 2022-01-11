import os
from flask_admin.base import AdminIndexView

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask import Flask
from flask_admin import Admin


from project.factory_helpers import config, ready_db
from project.blueprints import init_blueprints
from project.admin import AdminIndex, init_admin

db_password = os.environ.get("DB_PASS")

db = SQLAlchemy()
admin = Admin(name="Chronicler", template_mode="bootstrap3")
migrate_ = Migrate()
socketio = SocketIO(cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.refresh_view = "auth.reauth"
login_manager.login_message = "Please log in to access this page."
login_manager.needs_refresh_message = "Please reverify your credentials"


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
    admin.init_app(app, AdminIndex())
    migrate_.init_app(app, db, compare_type=True)
    ready_db(app, test_config)
    socketio.init_app(app)
    login_manager.init_app(app)
    init_blueprints(app)
    init_admin(admin, db)
    

    # register events file with application
    from project.events import notes

    # create db admins and orphanages
    from project.base_items import Base_items

    Base_items.init_database_assets(app)
    return app
