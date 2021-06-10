from flask import Flask, flash, redirect, render_template, request, session
# from flask_session import Session
from sqlalchemy.orm import backref
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash

from utils.dbclasses import *
from utils.BONhelpers import login_required

# Configure application
app = Flask(__name__)

# old SQLitedb
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///liteBON.db'
# Setting up MYSQL database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/BON'
# Secret Key
app.config['SECRET_KEY'] = 'is it secret?'
# Initialize the database
db = SQLAlchemy(app)


# Create form model
class UserForm(FlaskForm):
    username = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    hash = StringField("Hash", validators=[DataRequired ()])
    realname = StringField("Real Name")
    submit = SubmitField("Submit")

@app.route("/")
def index():
    # Show page listing all games
    # get list of games from db
    # games = db.execute('SELECT * FROM games')
    # games = Games.query.all()
    # check to see if the user is logged in
    # if session.get('user_id'):
    #     user = session.get('user_id')
    #     return render_template("index.html", games=games, user=user)
    # else:
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    # redirect user to main page after registring
    # clear variables and set wtforms
    name = None
    form = UserForm()
    list_users = Users.query.order_by(Users.date_added)
    if request.method == 'POST':
        user = Users.query.filter_by(email=form.email.data).first()
        if form.validate_on_submit():
            name = form.username.data
            # if email is unique add information to db
            if user is None:
                user = Users(username=form.username.data, email=form.email.data, hash=form.hash.data, realname=form.realname.data)
                db.session.add(user)
                db.session.commit()
                flash("Welcome to the table %s!" % form.realname.data)
                return redirect ('/')
            else:
                # if email is already in db alert user
                flash("%s is already in use!" % form.email.data)
                return render_template('register.html',
                    form = form,
                    name = name,
                    our_users=list_users,
                )
    else:
        return render_template("register.html", 
            form=form,
            name=name,
            our_users=list_users)

@app.route('/test_tables')
def test_tables():
    userheads = Users().head
    gameheads = Games().head
    charheads = Characters().head
    npcheads = NPCs().head
    placeheads = Places().head
    lootheads = Loot().head
    users = Users.query.all()
    return render_template('test_tables.html',
         userheads = userheads,
         gameheads = gameheads,
         charheads = charheads,
         npcheads = npcheads,
         placeheads = placeheads,
         lootheads = lootheads,
         users=users)

