import os
import json

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from project import forms
from project.models import Games, Players, Users, Images, Characters, Sessions, Notes
from project.helpers import nuke, attach_game_image_or_default_from_Images_model


# Variables
imageLink__buttonEdit = "/static/images/edit_button_image.png"
main = Blueprint('main', __name__)



#######################################
###            Index               ####
#######################################

@main.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    game_lists = Games.get_index_lists(current_user)

    return render_template("index.html"
        , games=game_lists["player_list"]
        , dm_games=game_lists["dm_list"])



#######################################
###            Join Game           ####
#######################################

@main.route('/join/<int:id_>', methods = ['POST', 'GET'])
@login_required
def join(id_):
    """serve list of games that User can join"""
    if id_ == 0:
        games=Games.query.filter(Games.dm_id != current_user.id).all()
        if len(games) > 1:
            for game in games:
                img = Images.query_from_id(game.img_id)
                if img:
                    game.image = attach_game_image_or_default_from_Images_model(img)
        return render_template("join.html"
            , games=games
        )
    else:
        return redirect(url_for('main.joining_get', id_=id_))

@main.route('/joining/<int:id_>', methods = ['GET'])
@login_required
def joining_get(id_):
    """serve new character form to User"""

    charform=forms.CharForm()
    game=Games.query.filter_by(id=id_).first()

    return render_template('joining.html',
        charform=charform,
        game=game)

@main.route("/joining/<int:id_>", methods = ["POST"])
@login_required
def joining_post(id_):
    """add new character to game"""

    charform=forms.CharForm()
    game=Games.query.filter_by(id=id_).first()
    game.image = game.image_object.img

    if not charform.charsubmit.data:
        return joining_failure("No character data sent to server", "alert-danger")
    image_id_or_failure_message = Images.upload("img")
    if type(image_id_or_failure_message) != int:
        return joining_failure(image_id_or_failure_message)
    Characters.create(name=charform.name.data, img_id=image_id_or_failure_message, bio=charform.bio.data, user_id=current_user.id, game_id=id_)
    Players.create(users_id=current_user.id, games_id=id_)
    return joining_success(id_, f"{charform.name.data} has joined the {game.name}!")

def joining_failure(id_, message):
    flash(message)
    return redirect(url_for('main.joining', id=id_))

def joining_success(id_, message):
    flash(message)
    return redirect(url_for('main.notes', id=id_))



#######################################
###            Create Game         ####
#######################################

@main.route('/create', methods=["GET", "POST"])
@login_required
def create():
    form = forms.CreateGameForm()
    if request.method.get == "GET":
        return render_template('create.html',
            gameform=form
            )
    else:
        if not forms.gamesubmit.data:
            return CreateGame.redirect_on_failure("No game data sent to server")
        image_id_or_exception = Images.upload("img") 
        if type(image_id_or_exception) != int:
            return CreateGame.redirect_on_failure(image_id_or_exception)
        game = Games.create(name=form.name.data, dm_id=current_user.id, img_id=image_id_or_exception, published=form.published.data)

        Characters.create(name="DM", user_id=current_user.id, game_id=game.id)
        Players.create(users_id=current_user.id, games_id=game.id)
        return CreateGame.redirect_on_success(game.id)

class CreateGame():

    @staticmethod
    def redirect_on_failure(message):
        flash(message)
        return redirect(url_for('main.create'))
    
    @staticmethod
    def redirect_on_success(id_):
        return redirect(url_for('main.notes', id=id_))



#######################################
###            Notes               ####
#######################################

@main.route('/notes/<int:game_id>', methods = ['GET'])
@login_required
def notes(game_id):

    tutorial = Users.get_admin()
    game=Games.query_from_id(game_id)
    session_list=Sessions.get_list_from_gameID(game_id)
    
    game_notes_by_session = {}
    if session_list is not None:

        for session in session_list:
            session_note_list = Notes.get_list_from_session_number(session.number, game_id)
            game_notes_by_session[session.number] = session_note_list

    js_note_dict = convert_to_JSON(game_notes_by_session)

    # this is to set the address for Flask socket.io
    heroku = False
    if os.environ.get("HEROKU_HOSTING"):
        heroku = True
        
    return render_template('notes/main.html'
        , tutorial=tutorial
        , js_note_dict=js_note_dict
        , edit_img=imageLink__buttonEdit
        , note_dict=game_notes_by_session
        , id=game_id
        , session_titles=session_list
        , game=game
        , heroku=heroku
    )

def convert_to_JSON(game_notes_by_session) -> dict:
    """ convert notes to JSON so that the js script attached to notes.html can insert the rich text.
     This has to be done because otherwise the html won't be able to read the mark up"""

    js_logs = {}
    for session in game_notes_by_session:
        js_logs[session] = []
        for note in game_notes_by_session[session]:
            js_logs[session].append([note.id, note.note])
    return json.dumps(js_logs)


@main.route('/profile')
@login_required
def profile():
    user = Users.query_from_id(current_user.id)
    return render_template('profile.html'
        , user=user
    )

@main.route('/nuked', methods=["GET"])
@login_required
def nuked():
    nuke()
    return "nuked"


