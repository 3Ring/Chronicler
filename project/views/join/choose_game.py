from flask import render_template

from project.models import Games


def choose_game_get():
    '''
    This function renders the join.html template and passes it a list of games that the user can join.
    
    :return: A list of games that the user can join.
    '''
    games = Games.get_my_joinable()
    return render_template("join/join.html", games=games)
