from flask import redirect, url_for, flash
from flask_login import logout_user


def logout_get():
    '''
    Logs out the user and redirects them to the login page
    :return: a redirect to the login page.
    '''
    flash("Successfully logged out")
    logout_user()
    return redirect(url_for("auth.login"))
