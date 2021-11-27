from flask import Blueprint, render_template, redirect, url_for, flash
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



@auth.route('/login', methods=['POST'])
def login_post():
    """checks data and logs in user if correct
    redirects user to index if they are already logged in
    """
    
    # check data
    form = forms.Login()
    user_found = form_validators.User.login(form)
    
    if not user_found:
        return redirect(url_for("auth.login"))

    # login user
    login_user(user_found, remember=form.remember.data)
    return redirect(url_for('main.index'))


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

@auth.route("/register", methods=['POST'])
def register_post():
    """register new users

    checks to make sure form is filled out correctly and redirects them to /login or back to /register
    (this is a redundancy as this is done client side as well)
    """

    form = forms.UserCreate()
    
    if not form_validators.User.register(form):
            return redirect(url_for('auth.register'))
    Users.create(name=form.name.data, email=form.email.data, password=form.password.data)
    return redirect(url_for('auth.login'))

            

#######################################
###            Logout              ####
#######################################

@auth.route('/logout')
@login_required
def logout():
    flash('Successfully logged out')
    logout_user()
    return redirect(url_for('auth.login'))
    