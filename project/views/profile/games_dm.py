from flask import render_template
from flask_login import current_user

from project.models import Games


def dm_get():
    """
    GET request function for "profile/games/dm.html"

    displays the games that the user is the DM for.
    :return: The rendered template for the dm games page.
    """
    dm_games = Games.get_personal_game_list_dm(current_user.id)
    return render_template("profile/games/dm.html", dm_games=dm_games)
