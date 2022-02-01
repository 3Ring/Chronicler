from flask import render_template, redirect, url_for
from flask_login import current_user

from project.forms.create_character import CharCreate
from project.forms.edit_game_player import CharAdd
from project.models import Games, Characters
from project.helpers.db_session import db_session


def join_game_get(game_id, game_name):
    """
    This function renders the joining.html template, which is used to join a game.

    :param game_id: The ID of the game to join
    :param game_name: The name of the game that the user is joining
    :return: A rendered template with the forms for joining a game.
    """

    my_characters = Characters.get_list_from_user(current_user.id)
    return render_template(
        "joining.html",
        charform=CharCreate(),
        addform=CharAdd(choices=my_characters),
        my_characters=my_characters,
        game=Games.query.get(int(game_id)),
    )


def join_game_post(game_id, game_name):
    """
    Validates and adds User's character to game.
    User may add existing character or create a new one.

    :param game_id: the id of the game to join
    :return: A redirect to the game's notes page.
    """
    game_id = int(game_id)
    with db_session() as sess:
        Games.add_player_to_game(game_id, current_user.id)
        my_characters = Characters.get_list_from_user(current_user.id)
        addform = CharAdd(choices=my_characters)
        charform = CharCreate()
        if addform.submit.data and addform.validate():
            return join_game_get(game_id, game_name)
        elif charform.submit.data and charform.validate():
            char = Characters.create(
                name=charform.name.data, bio=charform.bio.data, user_id=current_user.id
            )
            sess.flush()
            Characters.add_character_to_game(char.id, game_id)
        else:
            my_characters = Characters.get_list_from_user(current_user.id)
            return render_template(
                "joining.html",
                charform=charform,
                addform=addform,
                my_characters=my_characters,
                game=Games.query.get(int(game_id)),
            )
        return redirect(url_for("notes.game", game_id=game_id))

