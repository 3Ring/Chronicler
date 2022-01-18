from flask import render_template

from project.models import Games


def choose_game_get():
    """serve list of games that User can join"""
    games = Games.get_my_joinable()
    return render_template("join.html", games=games)
