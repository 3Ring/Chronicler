import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded (basically for debugging)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# setting up the database connection
con = sqlite3.connect('BON.db')
db = con.cursor()

@app.route("/")
@login_required
def index():
    """Show page listing all games"""
    # get list of games from db
    games = db.execute('SELECT * FROM games')
    # check to see if the user is logged in
    if session.get('user_id'):
        user = session.get('user_id')
        return render_template("index.html", games=games, user=user)
    else:
        return render_template("index.html", games=games)

        