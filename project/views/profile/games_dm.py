from flask import render_template
from flask_login import current_user

from project.models import Games


def dm_get():
    dm_games = Games.get_personal_game_list_dm(current_user.id)
    return render_template("profile/games/dm.html", dm_games=dm_games)
