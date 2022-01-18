from flask import Blueprint, request
from flask_login import fresh_login_required

from project.views.edit.account import (
    account_get,
    account_post,
    delete_get,
    delete_post,
)
from project.views.edit.character import character_get, character_post
from project.views.edit.game_dm import game_dm_get, game_dm_post
from project.views.edit.game_player import (
    add_remove_get,
    add_remove_post,
    leave_get,
    leave_post_,
)


edit = Blueprint("edit", __name__)


@edit.route("/edit/account", methods=["GET", "POST"])
@fresh_login_required
def account():
    if request.method == "GET":
        return account_get()
    return account_post()


@edit.route("/edit/account/delete", methods=["GET", "POST"])
@fresh_login_required
def delete_get():
    if request.method == "GET":
        return delete_get()
    return delete_post()


@edit.route("/edit/character/<int:character_id>", methods=["GET", "POST"])
@fresh_login_required
def character(character_id):
    if request.method == "GET":
        return character_get(character_id)
    return character_post(character_id)


@edit.route("/edit/games/dm/<int:game_id>", methods=["GET", "POST"])
@fresh_login_required
def game_dm(game_id):
    if request.method == "GET":
        return game_dm_get(game_id)
    return game_dm_post(game_id)


@edit.route("/edit/games/player/add_remove/<int:game_id>", methods=["GET", "POST"])
@fresh_login_required
def add_remove(game_id):
    if request.method == "GET":
        return add_remove_get(game_id)
    return add_remove_post(game_id)


@edit.route("/edit/games/player/leave/<int:game_id>", methods=["GET", "POST"])
@fresh_login_required
def leave(game_id):
    if request.method == "GET":
        return leave_get(game_id)
    return leave_post_(game_id)
