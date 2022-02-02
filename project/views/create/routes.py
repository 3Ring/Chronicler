from flask import Blueprint, request
from flask_login import login_required

from project.views.create.game import game_get, game_post
from project.views.create.dm import dm_get, dm_post
from project.views.create.character import character_get, character_post
from project.models import Games

create = Blueprint("create", __name__)


@create.route("/create/game", methods=["GET", "POST"])
@login_required
def game():
    if request.method == "GET":
        return game_get()
    return game_post()


@create.route("/create/dm/<int:game_id>", methods=["GET", "POST"])
@login_required
def dm(game_id):
    game = Games.query.get(game_id)
    if request.method == "GET":
        return dm_get(game)
    return dm_post(game)


@create.route("/create/character", methods=["GET", "POST"])
@login_required
def character():
    if request.method == "GET":
        return character_get()
    return character_post()
