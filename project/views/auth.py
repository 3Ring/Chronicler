from flask import Blueprint, render_template, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_login import current_user

from project.models import Users
from project import forms
from project import form_validators

auth = Blueprint('auth', __name__)


#######################################
###            Login               ####
#######################################

@auth.route('/login', methods=['GET'])
def login():
    """if user isn't logged in direct them to login page. 
    If the user is already logged in they will be directed to the index
    """

    if current_user.is_active:
        return redirect(url_for('main.index'))

    form = forms.Login()
    return render_template('login.html',
        form=form)

def _login_failure():
    return redirect(url_for("auth.login"))

def _login_success(user, form):
    login_user(user, remember=form.remember.data)
    return redirect(url_for("auth.login"))

@auth.route('/login', methods=['POST'])
def login_post():
    """checks data and logs in user if correct
    redirects user to index if they are already logged in
    """
    
    # check data
    form = forms.Login()
    if not form_validators.User.user(form):
        return _login_failure()
    user = Users.get_from_email(form.email.data)
    if not user:
        return _login_failure()
    if not form_validators.User.check_password(form.password.data, user.hashed_password):
        return _login_failure()
    # login user
    return _login_success(user, form)

def _reauth_failure():
    return redirect(url_for("auth.reauth"))

def _reauth_success(user, form):
    login_user(user, remember=form.remember.data)
    return redirect(url_for(session["reauth"]))

@auth.route('/reauth', methods=['GET'])
@login_required
def reauth():

    form = forms.Login()
    return render_template('login.html',
        form=form)

@auth.route('/reauth', methods=['POST'])
@login_required
def reauth_post():

    form = forms.Login()
    if not form_validators.User.user(form):
        return _login_failure()
    user = Users.get_from_email(form.email.data)
    if not user:
        return _reauth_failure()
    if not form_validators.User.check_password(form.password.data, user.hashed_password):
        return _reauth_failure()
    return _reauth_success(user, form)

#######################################
###           Register             ####
#######################################

@auth.route("/register", methods=['GET'])
def register():
    """direct user to registration page"""
    form = forms.UserCreate()
    return render_template(
        "register.html"
        , form=form
        )

def _register_failure():
    return redirect(url_for('auth.register'))

def _register_success():
    return redirect(url_for('auth.login'))

@auth.route("/register", methods=['POST'])
def register_post():
    """register new users

    checks to make sure form is filled out correctly and redirects them to /login or back to /register
    (this is a redundancy as this is done client side as well)
    """

    form = forms.UserCreate()
    
    if not form_validators.User.register(form):
        return _register_failure()
    if Users.get_from_email(form.email.data):
        flash(f"{form.email.data} is already in use!")
        return _register_failure()
    Users.create(name=form.name.data, email=form.email.data, password=form.password.data)
    return _register_success()

            

#######################################
###            Logout              ####
#######################################

@auth.route('/logout')
@login_required
def logout():
    flash('Successfully logged out')
    logout_user()
    return redirect(url_for('auth.login'))
    