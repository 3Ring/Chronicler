from flask import render_template
from flask_login import current_user

from project.models import Users


def account_get():
    """
    GET request function for "profile/account.html"

    display user's account information to them
    :return: The rendered template of the account.html page.
    """
    user = Users.query.get(current_user.id)
    return render_template("profile/account.html", user=user)
