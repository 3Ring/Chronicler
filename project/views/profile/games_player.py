from flask import render_template

from project.models import Games


def player_get(game_id):
    game = Games.query.get(game_id)
    return render_template("profile/games/player.html", game=game)
