from flask import Blueprint, request
from flask_login import login_required

from project.views.auth.login import login_get, login_post
from project.views.auth.register import register_get, register_post
from project.views.auth.logout import logout_get
from project.views.auth.reauth import reauth_get, reauth_post

auth = Blueprint("auth", __name__)


@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return login_get()
    return login_post()


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return register_get()
    return register_post()


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    return logout_get()


@auth.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "GET":
        return reauth_get()
    return reauth_post()
