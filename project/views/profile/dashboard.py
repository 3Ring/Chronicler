from flask import render_template
from flask_login import current_user

from project.models import Users


def dashboard_get():
    user = Users.query.get(current_user.id)
    return render_template("profile/dashboard.html", user=user)
