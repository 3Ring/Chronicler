from flask import render_template, redirect, url_for, flash
from flask_login import current_user

from project.forms.edit_game_player import LeaveGame
from project.models import BridgeGameCharacters, BridgeUserGames
from project.helpers.db_session import db_session


def leave_get(game):
    """
    GET request function for "edit/games/leave.html"

    It allows a user to leave a game.
    :param game: The SQLAlchemy game object
    :return: A rendered template with the game, forms.
    """
    leaveform = LeaveGame(game_id=game.id, game_name=game.name)
    return render_template("edit/games/leave.html", game=game, leaveform=leaveform)


def leave_post(game):
    """
    POST request function for "edit/games/leave.html"

    It allows a user to leave a game.
    :param game: The SQLAlchemy game object
    :return: A rendered template with the game, forms.
    """
    with db_session():
        leaveform = LeaveGame(game_id=game.id, game_name=game.name)
        if leaveform.validate_on_submit():
            leave(game)
            flash(f"You are no longer part of {game.name}")
            return redirect(url_for("main.index"))
        return render_template("edit/games/leave.html", game=game, leaveform=leaveform)


def leave(game):
    """
    Remove player and all of their characters from the game

    :param game: The SQLAlchemy game object
    """

    ptr_pcs = [c for c in current_user.get_character_list_from_game(game.id)]
    bgc = BridgeGameCharacters.query.filter_by(game_id=game.id).all()
    br_ids = set([br.character_id for br in bgc])
    pc_ids = set([c.id for c in ptr_pcs])
    char_ids_to_rm = pc_ids.intersection(br_ids)
    for br in bgc:
        if br.character_id in char_ids_to_rm:
            br.delete_self()
    player = BridgeUserGames.query.filter_by(
        game_id=game.id, user_id=current_user.id
    ).first()
    player.delete_self()

