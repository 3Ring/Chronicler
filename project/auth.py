from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .classes import *
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    form = LoginForm()
    try:
        if session['login_fail'] == True:
            fail = 'alert-warning'
        else:
            fail = 'alert-success'
        return render_template('login.html',
            form=form,
            fail=fail)
    except:
        return render_template('login.html',
            form=form)


@auth.route('/login', methods=['POST'])
def login_post():
    # (todo) make this work off email or username
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember')

    user = Users.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.hash, password):
        session['login_fail'] = True
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    session['login_fail'] = False
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))




@auth.route("/register", methods=['GET', 'POST'])
def register():
    # redirect user to main page after registring
    # clear variables and set wtforms
    name = None
    form = UserForm()
    if request.method == 'POST':
        if form.hash.data != form.confirm.data:
            flash("passwords do not match")
            return render_template('register.html',
                form = form,
                name = name,
                )
        else:
            user = Users.query.filter_by(email=form.email.data).first()
            if user == None:
                name = form.name.data
                # if email is unique add information to db
                user = Users(name=form.name.data, email=form.email.data, realname=form.realname.data, hash=generate_password_hash(form.hash.data, method='sha256'))
                db.session.add(user)
                db.session.commit()
                flash("Welcome to the table %s!" % form.realname.data)
                return redirect (url_for('auth.login'))
            else:
                # if email is already in db alert user
                flash("%s is already in use!" % form.email.data)
                return render_template('register.html',
                    form = form,
                    name = name,
                    )
    else:
        return render_template("register.html", 
            form=form,
            name=name,
            )

@auth.route('/logout')
@login_required
def logout():
    flash('Successfully logged out')
    logout_user()
    return redirect(url_for('auth.login'))