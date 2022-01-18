from flask import redirect, url_for, flash
from flask_login import logout_user


def logout_get():
    flash("Successfully logged out")
    logout_user()
    return redirect(url_for("auth.login"))
