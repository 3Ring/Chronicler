import os
import json

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from project import form_validators, forms
from project.defaults import Character
from project.models import BridgeGameCharacters, Games, BridgeUserGames, Users, Images, Characters, Sessions, Notes, NPCs
from project.helpers import attach_game_image_or_default_from_Images_model


# admin_pass = os.environ.
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
                img = Images.get_from_id(game.img_id)
                if img:
                    game.image = attach_game_image_or_default_from_Images_model(img)
        return render_template("join.html"
            , games=games
        )
    else:
        return redirect(url_for('main.joining', id_=id_))

@main.route('/joining/<int:id_>', methods = ['GET'])
@login_required
def joining(id_):
    """serve new character form to User"""

    charform=forms.CharCreate()
    game=Games.query.filter_by(id=id_).first()

    return render_template('joining.html',
        charform=charform,
        game=game)

@main.route("/joining/<int:id_>", methods = ["POST"])
@login_required
def joining_post(id_):
    """add new character to game"""

    charform=forms.CharCreate()
    game=Games.get_from_id(id_)
    

    if not charform.charsubmit.data:
        return joining_failure("No character data sent to server", "alert-danger")
    image_id_or_failure_message = Images.upload("img")
    if type(image_id_or_failure_message) != int:
        return joining_failure(image_id_or_failure_message)
    elif image_id_or_failure_message == -1:
        Characters.create(name=charform.name.data, bio=charform.bio.data, user_id=current_user.id, game_id=id_)
    else:
        Characters.create(name=charform.name.data, img_id=image_id_or_failure_message, bio=charform.bio.data, user_id=current_user.id, game_id=id_)
    BridgeUserGames.create(users_id=current_user.id, games_id=id_)
    return joining_success(id_, f"{charform.name.data} has joined the {game.name}!")

def joining_failure(id_, message):
    flash(message)
    return redirect(url_for('main.joining', id=id_))

def joining_success(id_, message):
    flash(message)
    return redirect(url_for('main.notes', game_id=id_))

#######################################
###            Notes               ####
#######################################

def get_game_character_list(game):
    if current_user.id == game.dm_id:
        character_list = [Games.get_dm_from_gameID(game.id)]
        npcs = NPCs.get_list(current_user.id)
        for npc in npcs:
            character_list.append(npc)
    else:
        character_list = [Characters.get_game_character_list(current_user.id, game.id)]
    choices = [(character) for character in character_list]
    return choices


@main.route('/notes/<int:game_id>', methods = ['GET'])
@login_required
def notes(game_id):
    print("dm", Games.get_dm_from_gameID(game_id).name)
    tutorial = Users.get_admin()
    game=Games.get_from_id(game_id)
    character_list = get_game_character_list(game)

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
    return render_template('notes/blueprint.html'
        , tutorial=tutorial
        , js_note_dict=js_note_dict
        , edit_img=imageLink__buttonEdit
        , note_dict=game_notes_by_session
        , id=game_id
        , session_titles=session_list
        , game=game
        , heroku=heroku
        , character_list = character_list
    )

def convert_to_JSON(game_notes_by_session) -> dict:
    """ convert notes to JSON so that the js script attached to notes.html can insert the rich text.
     This has to be done because otherwise the html won't be able to read the mark up"""

    js_logs = {}
    for session in game_notes_by_session:
        js_logs[session] = []
        for note in game_notes_by_session[session]:
            js_logs[session].append([note.id, note.text])
    return json.dumps(js_logs)

@main.route('/test')
def test():
    # Users.create(id=-1, name = "Chronicler", email="app@chronicler.gg", password=os.environ.get('ADMIN_PASS'))
    # print(Users.query.filter_by(name="test").first())
    # print(Characters.query.filter_by(id=-1).first())
    chars = Characters.query.with_entities(Characters.id, Characters.game_id).all()
    for char in chars:
        print(char.id)
        BridgeGameCharacters.create(game_id=char.game_id, character_id=char.id)
    bridge = BridgeGameCharacters.query.all()
    print(bridge)
    print(Characters.query.with_entities(Characters.game_id).all())

    return ""
# @main.route('/nuked', methods=["GET"])
# @login_required
# def nuked():
#     nuke()
#     return "nuked"

