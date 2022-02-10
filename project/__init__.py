import os

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask import Flask
from flask_admin import Admin


from project.setup_.config import config as config_app
from project.setup_.flask_login import config as config_fl
from project.setup_.flask_admin import init_admin
from project.setup_.helpers import update_db
from project.views.admin.routes import AdminIndex
from project.setup_.blueprints import init_blueprints
from project import events


db_password = os.environ.get("DB_PASS")

db = SQLAlchemy()
admin = Admin(name="Chronicler", template_mode="bootstrap3")
migrate_ = Migrate()
socketio = SocketIO(cors_allowed_origins="*")
login_manager = config_fl()

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    try:
        app = Flask(__name__)
        config_app(app)
        db.init_app(app)
        migrate_.init_app(app, db, compare_type=True)
        login_manager.init_app(app)
        init_admin(admin, db)
        admin.init_app(app, AdminIndex())
        socketio.init_app(app)
        init_blueprints(app)

        update_db(app, test_config)
        # from project.setup_.db_init_create.base_items import Base_items
        # Base_items.init_database_assets(app)
        return app
    except Exception as e:
        print(e)
