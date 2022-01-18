from flask import redirect, render_template, url_for
from flask_login import current_user

from project.models import Games, Users


def index_get():

    user = Users.query.get(current_user.id)
    game_lists = Games.get_index_lists(user)

    return render_template(
        "index.html", games=game_lists["player_list"], dm_games=game_lists["dm_list"]
    )


def index_post():
    games = Games.get_published()
    return render_template("join.html", games=games)
