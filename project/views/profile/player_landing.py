from flask import render_template
from flask_login import current_user

from project.models import Users


def landing_get():
    """
    GET request function for "profile/games/player_landing.html"

    This function returns the player game landing page
    :return: The rendered template of the player_landing.html page.
    """
    user = Users.query.get(current_user.id)
    player_games = user.get_game_list_player()
    return render_template(
        "profile/games/player_landing.html", player_games=player_games
    )
