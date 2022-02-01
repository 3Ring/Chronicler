from flask import render_template, flash
from flask_login import current_user

from project.forms.create_character import CharCreate
from project.forms.edit_game_player import CharAdd
from project.forms.edit_dm_game import RemoveCharacter
from project.models import BridgeGameCharacters, Characters
from project.helpers.db_session import db_session
from project.views.edit.game_dm import remove_character
from project.views.create.character import create_character


def add_remove_get(game):
    '''
    GET request function for "edit/games/add_remove.html"

    This function is used to add and remove characters from a game. 
    :param game: The SQLAlchemy game object
    :return: A rendered template with the game and forms.
    '''
    return render(game)


def add_remove_post(game):
    '''
    POST request function for "edit/games/add_remove.html"
    This function is used to add and remove characters from a game. 
    
    :param game: The SQLAlchemy game object
    :return: A rendered template with the game and forms.
    '''
    with db_session() as sess:
        charform = CharCreate(prefix="a")
        choices = make_choices(game)
        addform = CharAdd(prefix="b", game_id=game.id, choices=choices)
        removeform = RemoveCharacter(
            prefix="c",
            game_id=game.id,
            choices=current_user.get_character_list_from_game(game.id),
        )
        if addform.submit.data:
            if addform.validate():
                Characters.add_character_to_game(addform.character.data, game.id)
                flash(
                    f"{Characters.query.get(addform.character.data).name} added to {game.name}!"
                )
                return render(game)
        elif charform.submit.data:
            if charform.validate():
                new = create_character(charform)
                sess.flush()
                Characters.add_character_to_game(new.id, game.id)
                flash(f"{new.name} successfully added to {game.name}")
                return render(game)
        elif removeform.submit.data:
            if removeform.validate():
                remove_character(game, removeform)
                return render(game)
        return render(game, charform=charform, addform=addform, removeform=removeform)


def render(game, charform=None, addform=None, removeform=None):
    '''
    This function renders the add/remove character page for a game

    :param game: The SQLAlchemy game object

    :param charform: The form that allows you to create a new character
    :param addform: The form that allows you to add an existing character to the game
    :param removeform: The form that will be used to remove characters from the game
    :return: The rendered template.
    '''
    if charform is None:
        charform = CharCreate(prefix="a")
    if addform is None:
        choices = make_choices(game)
        addform = CharAdd(prefix="b", game_id=game.id, choices=choices)

    if removeform is None:
        removeform = RemoveCharacter(
            prefix="c",
            game_id=game.id,
            choices=current_user.get_character_list_from_game(game.id),
        )
    return render_template(
        "edit/games/add_remove.html",
        game=game,
        addform=addform,
        charform=charform,
        removeform=removeform,
    )


def make_choices(game):
    '''
    It returns a list of characters that are not in the game.
    
    :param game: The SQLAlchemy game object
    :return: A list of characters that are not in the game.
    '''
    characters = Characters.query.filter_by(user_id=current_user.id).all()
    bridges = BridgeGameCharacters.query.filter_by(game_id=game.id).all()
    hm = {}
    [hm.update({b.character_id: True}) for b in bridges]
    choices = []
    for c in characters:
        if not hm.get(c.id, None) and not c.avatar and not c.dm:
            choices.append(c)
    return choices
