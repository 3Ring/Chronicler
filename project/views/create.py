import os
import json

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from project import form_validators, forms
from project.models import BridgeGameCharacters, Games, BridgeUserGames, Users, Images, Characters, Sessions, Notes
from project.helpers import attach_game_image_or_default_from_Images_model

create = Blueprint('create', __name__)


#######################################
###              Game              ####
#######################################

@create.route('/create/game', methods=["GET"])
@login_required
def game():

    form = forms.GameCreate()
    return render_template('create/game.html',
        gameform=form
        )

@create.route('/create/game', methods=["POST"])
@login_required
def game_post():

    form = forms.GameCreate()
    success = form_validators.Game.create(form)
    if not success:
        print("not success")
        return redirect(url_for("create.game"))
    elif success == "no image":
        img_id = None
        print("no image")
    else:
        img_id = Images.upload(success["pic"], success["secure_name"], success["mimetype"]) 
        print("img_id", img_id)
    game = Games.create(name=form.name.data
                    , dm_id=current_user.id
                    , published=form.published.data
                    , img_id=img_id
                    )
    
    return redirect(url_for("create.dm"
                        , game_id=game.id
                        ))

#######################################
###          DM Character          ####
#######################################


@create.route('/create/dm/<int:game_id>', methods=["GET"])
@login_required
def dm(game_id):
    print("get")
    game = Games.get_from_id(game_id)
    form = forms.DMCreate()
    dm_default_image = "/static/images/default_dm.jpg"
    return render_template("create/dm.html"
        , game = game
        , form = form
        , dm_default_image = dm_default_image
        )

@create.route('/create/dm/<int:game_id>', methods=["POST"])
@login_required
def dm_post(game_id):

    form = forms.DMCreate()
    success = form_validators.Character.dm_create(form)
    if not success:
        return redirect(url_for("create.dm", game_id=game_id))
    elif success == "no image":
        img_id = None
    else:
        img_id = Images.upload(success["pic"], success["secure_name"], success["mimetype"]) 

    avatar = Characters.create(name=form.name.data
                        , dm=True
                        , user_id=current_user.id
                        , img_id=img_id
                        )
    BridgeGameCharacters.create(dm=True
                                , character_id=avatar.id
                                , game_id=game_id
                                )

    return redirect(url_for("notes.game", game_id=game_id))


#######################################
###            Character           ####
#######################################

@create.route('/create/character', methods=["GET"])
@login_required
def character():
    form = forms.CharCreate()
    return render_template("/create/character.html"
                            , form=form
                            )

@create.route('/create/character', methods=["POST"])
@login_required
def character_post():

    form = forms.CharCreate()
    success = form_validators.Character.create(form)
    if not success:
        return redirect(url_for("create.character"))
    elif success == "no image":
        img_id = None
    else:
        img_id = Images.upload(success["pic"], success["secure_name"], success["mimetype"]) 

    Characters.create(name=form.name.data
                        , bio=form.bio.data
                        , user_id=current_user.id
                        , img_id=img_id
                        )

    return redirect(url_for("profile.characters"))
