from flask import Blueprint, flash, redirect, render_template, request, session, url_for
# from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import generate_password_hash

from .classes import *
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/test_tables', methods = ['GET', 'POST'])
@login_required
def test_tables():

    # make sure that only the admin can access this site
    if not current_user.id == 1:
        return redirect(url_for('main.profile'))
    
    # set variable so Flask can build the site
    userheads = Users().head
    users = Users.query.all()
    gameheads = Games().head
    games = Games.query.all()
    charheads = Characters().head
    npcheads = NPCs().head
    placeheads = Places().head
    lootheads = Loot().head


    userform = UserForm()
    gameform = GameForm()
    delform = DeleteForm()

    if request.method == 'POST':
        if gameform.gamesubmit.data:

            game = Games(name=gameform.name.data, imglink=gameform.imglink.data, sessions=gameform.sessions.data, secret=gameform.secret.data, dm_id=gameform.dm_id.data)
            db.session.add(game)
            db.session.commit()
            games = Games.query.all()
        elif userform.usersubmit.data:

            user = Users(name=userform.name.data, email=userform.email.data, realname=userform.realname.data, hash=generate_password_hash(userform.hash.data, method='sha256'))
            db.session.add(user)
            db.session.commit()
            users = Users.query.all()

    delform.user_group_id.choices = [(g.id) for g in Users.query.order_by('id')]
    delform.game_group_id.choices = [(g.id) for g in Games.query.order_by('id')]
    return render_template('test_tables.html',
        userheads = userheads,
        gameheads = gameheads,
        charheads = charheads,
        npcheads = npcheads,
        placeheads = placeheads,
        lootheads = lootheads,
        users = users,
        games = games,
        delform = delform,
        userform = userform,
        gameform = gameform)

@main.route('/confirming', methods = ['POST'])
@login_required
def post_test_tables():
    delete = DeleteForm()
    if delete.user_group_id.data:
        delete_id = delete.user_group_id.data
        deleted = Users.query.filter_by(id = delete_id).first()
        session['table_to_edit'] = 'Users'
    elif delete.game_group_id.data:
        delete_id = delete.game_group_id.data
        deleted = Games.query.filter_by(id = delete_id).first()
        session['table_to_edit'] = 'Games'
    session['name_to_delete'] = deleted.name
    session['id_to_delete'] = delete_id
    flash("Are you sure you want to delete %s?" % session['name_to_delete'])
    form = ConForm()
    return render_template('confirm.html',
    form = form,
    name = session['name_to_delete'])

@main.route('/confirm', methods = ['POST'])
@login_required
def confirm():
    form = ConForm()
    if session['table_to_edit'] == 'Users':
        row_to_delete = Users.query.filter_by(id = session.get('id_to_delete')).first()
    elif session['table_to_edit'] == 'Games':
        row_to_delete = Games.query.filter_by(id = session.get('id_to_delete')).first()
    # if the cancel button is pressed
    if form.cancel.data:
        return redirect(url_for('main.test_tables'))
    # if data is submitted correctly and matches
    elif form.todelete.data == row_to_delete.name:
        # delete user
        flash("%s has been successfully deleted" % session['name_to_delete'])
        db.session.delete(row_to_delete)
        db.session.commit()
        return redirect(url_for('main.test_tables'))
    # if data is entered incorrectly
    else:
        flash("names do not match, check to make sure you are deleting the correct user")
        deleted = Users.query.filter_by(id = session.get('idtodelete')).first()
        return render_template('confirm.html',
        form = form,
        name = deleted.name)

@main.route('/test', methods = ['POST', 'GET'])
def test():
    form = TableForm()
    form.group_id.choices = ['Users', 'Games']
    if request.method == 'GET':
        return render_template('test.html',
            form=form)
