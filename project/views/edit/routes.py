from flask import Blueprint, request
from flask_login import fresh_login_required, current_user

from project.models import Characters, Games
from project.views.helpers import not_authorized
from project.views.edit.account import (
    account_get,
    account_post,
    delete_get,
    delete_post,
)
from project.views.edit.character import character_get, character_post
from project.views.edit.game_dm import game_dm_get, game_dm_post
from project.views.edit.game_player import add_remove_get, add_remove_post
from project.views.edit.leave import leave_get, leave_post


edit = Blueprint("edit", __name__)


@edit.route("/edit/account", methods=["GET", "POST"])
@fresh_login_required
def account():
    if request.method == "GET":
        return account_get()
    return account_post()


@edit.route("/edit/account/delete", methods=["GET", "POST"])
@fresh_login_required
def delete():
    if request.method == "GET":
        return delete_get()
    return delete_post()


@edit.route("/edit/character/<int:character_id>", methods=["GET", "POST"])
@fresh_login_required
def character(character_id):
    character = Characters.query.get(character_id)
    if character.user_id != current_user.id:
        return not_authorized()
    if request.method == "GET":
        return character_get(character)
    return character_post(character)


@edit.route("/edit/games/dm/<int:game_id>", methods=["GET", "POST"])
@fresh_login_required
def game_dm(game_id):
    game = Games.query.get(game_id)
    if current_user.id != game.dm_id:
        return not_authorized()
    if request.method == "GET":
        return game_dm_get(game)
    return game_dm_post(game)


@edit.route("/edit/games/player/add_remove/<int:game_id>", methods=["GET", "POST"])
@fresh_login_required
def add_remove(game_id):
    game = Games.query.get(game_id)
    if not current_user in Games.get_player_list_from_id(game_id):
        return not_authorized()
    if request.method == "GET":
        return add_remove_get(game)
    return add_remove_post(game)


@edit.route("/edit/games/player/leave/<int:game_id>", methods=["GET", "POST"])
@fresh_login_required
def leave(game_id):
    game = Games.query.get(game_id)
    if not current_user in Games.get_player_list_from_id(game_id):
        return not_authorized()
    if request.method == "GET":
        return leave_get(game)
    return leave_post(game)
