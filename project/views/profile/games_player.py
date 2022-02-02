from flask import render_template

from project.models import Games


def player_get(game_id):
    '''
    GET request function for "profile/games/player.html"

    Displays the games that the user is part of and a link to the join new game route
    
    :param game_id: The id of the game that you want to view
    :return: The player profile page.
    '''
    game = Games.query.get(game_id)
    return render_template("profile/games/player.html", game=game)
