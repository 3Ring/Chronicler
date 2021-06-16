from flask import Blueprint, flash, redirect, render_template, request, session, url_for
# from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash

from .classes import *
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

@main.route("/")
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

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

@main.route('/test_tables')
@login_required
def test_tables():
    userheads = Users().head
    gameheads = Games().head
    charheads = Characters().head
    npcheads = NPCs().head
    placeheads = Places().head
    lootheads = Loot().head
    users = Users.query.all()

    form = DeleteForm()
    form.group_id.choices = [(g.id) for g in Users.query.order_by('id')]

    return render_template('test_tables.html',
         userheads = userheads,
         gameheads = gameheads,
         charheads = charheads,
         npcheads = npcheads,
         placeheads = placeheads,
         lootheads = lootheads,
         users = users,
         form = form)

@main.route('/test_tables', methods = ['POST'])
@login_required
def post_test_tables():
    delform = DeleteForm()
    delete_id = delform.group_id.data
    deleted = Users.query.filter_by(id = delete_id).first()
    session['idtodelete'] = delete_id
    session['nametodelete'] = deleted.username
    flash("Are you sure you want to delete %s?" % session['nametodelete'])
    form = ConForm()
    return render_template('confirm.html',
    form = form,
    name = deleted.username)

@main.route('/confirm', methods = ['GET', 'POST'])
@login_required
def confirm():
    if request.method == 'POST':
        form = ConForm()
        usertodelete = Users.query.filter_by(id = session.get('idtodelete')).first()
        name = usertodelete.username
        if form.cancel.data:
            return redirect(url_for('main.test_tables'))
        elif form.todelete.data == usertodelete.username:
            # delete user
            flash("%s has been successfully deleted" % session['nametodelete'])
            db.session.delete(usertodelete)
            db.session.commit()
            return redirect(url_for('main.test_tables'))
        else:
            flash("names do not match, check to make sure you are deleting the correct user")
            deleted = Users.query.filter_by(id = session.get('idtodelete')).first()
            return render_template('confirm.html',
            form = form,
            name = deleted.username)

