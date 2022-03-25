
from project.extensions.migrate import migrate
from project.extensions.sql_alchemy import db
from project.extensions.socketio import socketio
from project.extensions.login import login_manager
from project.extensions.login import config as flask_login_config
from project.extensions.admin import admin, init_admin
from project.views.admin.routes import AdminIndex

def configure_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    flask_login_config()
    login_manager.init_app(app)
    init_admin(admin, db)
    admin.init_app(app, AdminIndex())
    socketio.init_app(app)

