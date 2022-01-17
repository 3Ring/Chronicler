from flask import Blueprint, render_template, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_login import current_user

from project.__init__ import db
from project.helpers.db_session import db_session
from project.models import Users, Characters, Games
from project import forms
from project import form_validators

auth = Blueprint("auth", __name__)


#######################################
###            Login               ####
#######################################


@auth.route("/login", methods=["GET"])
def login():
    """if user isn't logged in direct them to login page.
    If the user is already logged in they will be directed to the index
    """

    if current_user.is_active:
        return redirect(url_for("main.index"))

    form = forms.Login()
    return render_template("login.html", form=form)


def _login_failure():
    # flash("incorrect")
    return redirect(url_for("auth.login"))





@auth.route("/login", methods=["POST"])
def login_post():
    """checks data and logs in user if correct
    redirects user to index if they are already logged in
    """

    # check data
    form = forms.Login()
    user = Users.query.filter_by(email=form.email.data).first()
    print(f'user: {user}')
    if not form.validate_on_submit():
        print(f'no')
    # if not form_validators.User.user(form):
        return _login_failure()
    # if not user:
    #     return _login_failure()
    # if not form_validators.User.check_password(
    #     form.password.data, user.hashed_password
    # ):
    #     return _login_failure()
    # login user
    login_user(user, remember=form.remember.data)
    return redirect(url_for("main.index"))



def _reauth_failure():
    return redirect(url_for("auth.reauth"))


def _reauth_success(user, form):
    login_user(user, remember=form.remember.data)
    return redirect(url_for(session["reauth"]))


@auth.route("/reauth", methods=["GET"])
@login_required
def reauth():

    form = forms.Login()
    return render_template("login.html", form=form)


@auth.route("/reauth", methods=["POST"])
@login_required
def reauth_post():

    form = forms.Login()
    if not form_validators.User.user(form):
        return _login_failure()
    user = Users.query.filter_by(email=form.email.data)
    if not user:
        return _reauth_failure()
        
    if not form_validators.User.check_password(
        form.password.data, user.hashed_password
    ):
        return _reauth_failure()
    return _reauth_success(user, form)


#######################################
###           Register             ####
#######################################


@auth.route("/register", methods=["GET"])
def register():
    """direct user to registration page"""
    form = forms.UserCreate()
    return render_template("register.html", form=form)

@auth.route("/register", methods=["POST"])
def register_post():
    """register new users"""
    form = forms.UserCreate()
    if not form.validate_on_submit():
        return render_template("register.html", form=form)
    # with db_session():
    #     user = Users.create(
    #         name=form.name.data,
    #         email=form.email.data,
    #         password=form.password.data,
    #     )
    # add_to_bug_report_page(user)
    return redirect(url_for("auth.login"))

   
def add_to_bug_report_page(user):
    """Creates a User character and adds them to the bug report page
    it's done this way because the bug report page uses the "notes" page's code so it requires a "Character".
    
    uses multiple commits/rollbacks due to foreign key requirements
    """
    with db_session():
        try:
            avatar = Characters.create(name=user.name, user_id=user.id, avatar=True)
        except Exception:
            db.session.rollback()
            user.delete_self()
            db.session.commit()
            raise
    with db_session():
        try:
            avatar.add_to_game(Games.get_bugs().id)
        except Exception:
            db.session.rollback()
            avatar.delete_self()
            user.delete_self()
            db.session.commit()
            raise

#######################################
###            Logout              ####
#######################################


@auth.route("/logout")
@login_required
def logout():
    flash("Successfully logged out")
    logout_user()
    return redirect(url_for("auth.login"))
