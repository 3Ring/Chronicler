
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from .settings import app

db = SQLAlchemy(app)
# print("check1")
socketio = SocketIO(app, logger=True, engineio_logger=True)
# print("check2")

def create_app():

    migrate = Migrate(app, db)
    from .classes import Users

    db.init_app(app)
    # print("check3")
    socketio.init_app(app)
    # print("check4")
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app) 
    # print("check5")

    # provide login_manager with a unicode user ID
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    # blueprint for auth routes of app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .BONapp import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app