from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_login import current_user

from .classes import *



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

    form = LoginForm()
    return render_template('login.html',
        form=form)

def login_failure(message=None):
    """Redirect user to login page with flashed message"""
    if message:
        flash(message)
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    """checks data and logs in user if correct
    redirects user to index if they are already logged in
    """
    
    # check data
    form = LoginForm()
    user_in_db = Users.query.filter_by(email=form.email.data).first()
    if not user_in_db or not check_password_hash(user_in_db.hashed_password, form.password.data):
        return login_failure('Please check your login details and try again.')

    # login user
    login_user(user_in_db, remember=form.remember.data)
    return redirect(url_for('main.index'))


#######################################
###           Register             ####
#######################################

@auth.route("/register", methods=['GET'])
def register():
    """direct user to registration page"""

    form = UserForm()
    return render_template(
        "register.html"
        , form=form
        )

def register_failure(message=None):
    """redirect user back to /register on failure with flashed message"""

    if message:
        flash(message)
    return redirect(url_for('auth.register'))
    
def register_success(message=None):
    """redirect user to /login on successful registration"""

    if message:
        flash(message)
    return redirect(url_for('auth.login'))

@auth.route("/register", methods=['POST'])
def register_post():
    """register new users

    checks to make sure form is filled out correctly and redirects them to /login or back to /register
    (this is a redundancy as this is done client side as well)
    """

    form = UserForm()
    # check if all required data was submitted
    if not form.password.data or not form.email.data or not form.name.data or not form.confirm.data:
        return register_failure("missing form data")
    # check that passwords match
    elif form.password.data != form.confirm.data:
        return register_failure("passwords do not match")
    else:
        user = Users.query.filter_by(email=form.email.data).first()
        # check to make sure email is unique
        if user == None:
            Users.create(name=form.name.data, email=form.email.data, password=form.password.data)
            return register_success("Welcome to the table %s!" % form.name.data)
        else:
            # if email is already in db alert user
            return register_failure("%s is already in use!" % form.email.data)
            

#######################################
###            Logout              ####
#######################################

@auth.route('/logout')
@login_required
def logout():
    flash('Successfully logged out')
    logout_user()
    return redirect(url_for('auth.login'))
    