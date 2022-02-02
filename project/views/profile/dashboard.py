from flask import render_template
from flask_login import current_user

from project.models import Users


def dashboard_get():
    """
    GET request function for "profile/dashboard.html"

    Landing page for profile
    :return: The rendered dashboard.html template.
    """
    user = Users.query.get(current_user.id)
    return render_template("profile/dashboard.html", user=user)
