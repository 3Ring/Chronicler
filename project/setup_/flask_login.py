from flask_login import LoginManager

login_manager = LoginManager()


def config():
    login_manager.login_view = "auth.login"
    login_manager.refresh_view = "auth.reauth"
    login_manager.login_message = "Please log in to access this page."
    login_manager.needs_refresh_message = "Please reverify your credentials"
    return login_manager


@login_manager.user_loader
def load_user(user_id):
    """provide login_manager with a unicode user ID"""
    from project.models import Users

    return Users.query.get(int(user_id))
