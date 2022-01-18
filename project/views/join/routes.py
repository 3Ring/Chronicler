from flask import Blueprint, request
from flask_login import login_required

from project.views.join.choose_game import choose_game_get
from project.views.join.join_game import join_game_get, join_game_post

join = Blueprint("join", __name__)


@join.route("/join", methods=["GET"])
@login_required
def game():
    return choose_game_get()


@join.route("/joining/<game_id>/<game_name>", methods=["GET", "POST"])
@login_required
def joining(game_id, game_name):
    if request.method == "GET":
        return join_game_get(game_id, game_name)
    return join_game_post(game_id, game_name)
