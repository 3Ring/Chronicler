from flask import render_template, redirect, url_for
from flask_login import current_user

from project.forms.create_character import CharCreate
from project.forms.edit_game_player import CharAdd
from project.models import Games, Characters
from project.helpers.db_session import db_session


def join_game_get(game):
    """
    GET request function for "join/joining.html"

    called when a user is joining a new game.
    :param game: The SQLAlchemy game object
    :return: The rendered "joining" template
    """
    return render(game)


def join_game_post(game):
    """
    POST request function for "join/joining.html"

    Adds a player to a game.
    :param game: The SQLAlchemy game object
    :return: redirects user to game they just joined
    """
    with db_session() as sess:
        Games.add_player_to_game(game.id, current_user.id)
        my_characters = Characters.get_list_from_user(current_user.id)
        addform = CharAdd(prefix="add", game_id=game.id, choices=my_characters)
        charform = CharCreate(prefix="create")
        if addform.submit.data and addform.validate():
            for character_id in addform.character.data:
                Characters.add_character_to_game(character_id, game.id)
            return redirect(url_for("notes.game", game_id=game.id))
        elif charform.submit.data and charform.validate():
            char = Characters.create(
                name=charform.name.data, bio=charform.bio.data, user_id=current_user.id
            )
            sess.flush()
            Characters.add_character_to_game(char.id, game.id)
            return redirect(url_for("notes.game", game_id=game.id))
        return render(game, charform=charform, addform=addform)


def render(game, charform=None, addform=None):
    """
    Render the joining page

    :param game: The SQLAlchemy game object
    :param charform: The form that the user will use to create a new character
    :param addform: The form that allows you to add an existing character to the game
    :return: The rendered template.
    """
    my_characters = Characters.get_list_from_user(current_user.id)
    if not charform:
        charform = CharCreate(prefix="create")
    if not addform:
        addform = CharAdd(prefix="add", game_id=game.id, choices=my_characters)
    return render_template(
        "join/joining.html",
        charform=charform,
        addform=addform,
        my_characters=my_characters,
        game=game,
        size=len(my_characters)
    )
