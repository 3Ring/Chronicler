from flask import Blueprint
from flask_login import login_required

from project.views.profile.dashboard import dashboard_get
from project.views.profile.account import account_get
from project.views.profile.characters import characters_get
from project.views.profile.games import games_get
from project.views.profile.player_landing import landing_get
from project.views.profile.games_player import player_get
from project.views.profile.games_dm import dm_get


profile = Blueprint("profile", __name__)


@profile.route("/profile", methods=["GET"])
@login_required
def dashboard():
    return dashboard_get()


@profile.route("/profile/account", methods=["GET"])
@login_required
def account():
    return account_get()


@profile.route("/profile/characters", methods=["GET"])
@login_required
def characters():
    return characters_get()


@profile.route("/profile/games", methods=["GET"])
@login_required
def games():
    return games_get()


@profile.route("/profile/games/player", methods=["GET"])
@login_required
def player_landing():
    return landing_get()


@profile.route("/profile/games/player/<int:game_id>", methods=["GET"])
@login_required
def player(game_id):
    return player_get(game_id)


@profile.route("/profile/games/dm", methods=["GET"])
@login_required
def dm():
    return dm_get()
