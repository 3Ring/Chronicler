from flask import render_template
from flask_login import current_user

from project.models import Games, Users


def index_get():
    '''
    GET request function for "index.html"

    Get the current user's games to display
    :return: a rendered template
    '''
    user = Users.query.get(current_user.id)
    game_lists = Games.get_index_lists(user)
    return render_template(
        "index/index.html", games=game_lists["player_list"], dm_games=game_lists["dm_list"]
    )
