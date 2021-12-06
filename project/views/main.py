import os
import json

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from project import form_validators, forms
from project.defaults import Character
from project.models import (
    BridgeGameCharacters,
    Games,
    BridgeUserGames,
    Users,
    Images,
    Characters,
    Sessions,
    Notes,
    NPCs,
)
from project.helpers import attach_game_image_or_default_from_Images_model


# admin_pass = os.environ.
# Variables
imageLink__buttonEdit = "/static/images/edit_button_image.png"
main = Blueprint("main", __name__)


#######################################
###            Index               ####
#######################################


@main.route("/", methods=["GET"])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    user = Users.get_from_id(current_user.id)
    game_lists = Games.get_index_lists(user)

    return render_template(
        "index.html", games=game_lists["player_list"], dm_games=game_lists["dm_list"]
    )


@main.route("/", methods=["POST"])
@login_required
def index_post():
    games = Games.get_published()
    return render_template("join.html", games=games)


######################################
##            Join Game           ####
######################################


@main.route("/test")
def test():
    game = Games.get_from_id(5)
    return render_template("test.html", game=game)


@main.route("/test/<game_id>/<game_name>")
def test_case(game_id, game_name):
    return ""
