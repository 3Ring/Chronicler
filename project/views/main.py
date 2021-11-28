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

@main.route("/", methods = ['GET'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    game_lists = Games.get_index_lists(current_user)

    return render_template("index.html"
        , games=game_lists["player_list"]
        , dm_games=game_lists["dm_list"])

@main.route("/", methods = ['POST'])
@login_required
def index_post():
    games = Games.get_published()
    return render_template("join.html"
        , games=games
    )
######################################
##            Join Game           ####
######################################

@main.route('/join', methods = ['GET'])
@login_required
def join():
    """serve list of games that User can join"""
    games = Games.get_published()
    return render_template("join.html"
        , games=games
    )
    # if id_ == 0:
    #     games=Games.query.filter(Games.dm_id != current_user.id).all()
    #     if len(games) > 1:
    #         for game in games:
    #             img = Images.get_from_id(game.img_id)
    #             if img:
    #                 game.image = attach_game_image_or_default_from_Images_model(img)
    #     return render_template("join.html"
    #         , games=games
    #     )
    # else:
    #     return redirect(url_for('main.joining', id_=id_))

@main.route('/joining/<int:id_>', methods = ['GET'])
@login_required
def joining(id_):
    """Serve new character form to User"""

    my_characters = Characters.get_list_from_userID(current_user.id)
    charform=forms.CharCreate()
    charform.character.choices = ["Make New Character"]
    for g in my_characters:
        charform.character.choices.append(g.name)
    game=Games.get_from_id(id_)

    return render_template('joining.html'
        , charform=charform
        , my_characters=my_characters
        , game=game
        )

@main.route("/joining/<int:id_>", methods = ["POST"])
@login_required
def joining_post(id_):
    return
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

