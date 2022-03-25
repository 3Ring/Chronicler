from flask import Blueprint, request, redirect, url_for
from flask_login import login_required, current_user

from project.views.auth.login import login_get, login_post
from project.views.auth.register import register_get, register_post
from project.views.auth.logout import logout_get
from project.views.auth.reauth import reauth_get, reauth_post

auth = Blueprint("auth", __name__)


@auth.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index.page"))
    if request.method == "GET":
        return login_get()
    return login_post()


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index.page"))
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
    if not request.args.get("next"):
        return redirect(url_for("index.page"))
    if request.method == "GET":
        return reauth_get()
    return reauth_post()
