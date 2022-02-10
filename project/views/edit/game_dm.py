from sys import prefix
from flask import render_template, flash, redirect, url_for
from project.forms.edit_dm_game import (
    Edit,
    Delete,
    RemovePlayer,
    RemoveCharacter,
)
from project.helpers.db_session import db_session

from project.models import (
    BridgeGameCharacters,
    BridgeGameItems,
    BridgeGameNPCs,
    BridgeGamePlaces,
    BridgeUserGames,
    Notes,
    Characters,
    Sessions,
    Users,
    Games,
    Images,
)


def game_dm_get(game):
    """
    GET request function for "edit/games/dm.html"

    This function is called when a user wants to edit a game's details or delete a game
    :param game: The SQLAlchemy game object
    :return: A rendered template with the game, players, and forms.
    """
    return render(game)


def game_dm_post(game):
    """
    POST request function for "edit/games/dm.html"
    
    This function is called when a user wants to edit a game's details or delete a game
    :param game: The SQLAlchemy game object
    :return: A rendered template with the game, players, and forms.
    """

    error_target = None
    form_edit = Edit(prefix="edit")
    form_delete = Delete(prefix="del")
    form_players = RemovePlayer(prefix="rm_player", choices=Games.get_player_list_from_id(game.id))
    form_characters = RemoveCharacter(prefix="rm_character", choices=Games.get_PCs(game.id))
    with db_session(autocommit=False) as sess:
        if form_edit.submit.data:
            if form_edit.validate():
                edit_game_details(game, form_edit)
                sess.commit()
                return render(game)
        elif form_delete.game_delete_submit.data:
            if form_delete.validate():
                delete_game_and_assets(game)
                sess.commit()
                flash(f"{game.name} and all assets deleted successfully")
                return redirect(url_for("index.page"))
            error_target = "del_game"
        elif form_players.players.data:
            if form_players.validate():
                remove_player(game, form_players)
                sess.commit()
                return render(game)
            error_target = "rm_player"
        elif form_characters.characters.data:
            if form_characters.validate():
                remove_character(game, form_characters)
                sess.commit()
                return render(game)
            error_target = "rm_character"
        return render(
            game,
            form_edit=form_edit,
            form_delete=form_delete,
            form_players=form_players,
            form_characters=form_characters,
            error_target=error_target,
        )


def render(
    game,
    form_edit=None,
    form_delete=None,
    form_players=None,
    form_characters=None,
    error_target=None,
):
    """
    Render the game's edit page

    :param game: The SQLAlchemy game object
    :param form_edit: The form that will be used to edit the game
    :param form_delete: The form that will be used to delete the game
    :param form_players: This is the form that will be used to remove players from the game
    :param form_characters: This is the form that will be used to remove characters from the game
    :param error_target: This is the 'data-form' attribute value attached to the form that has errors if applicable. Used to reveal said form.
    """
    if form_edit is None:
        form_edit = Edit(prefix="edit")
    if form_delete is None:
        form_delete = Delete(prefix="del")
    if form_players is None:
        form_players = RemovePlayer(prefix="rm_player", choices=Games.get_player_list_from_id(game.id))
    if form_characters is None:
        form_characters = RemoveCharacter(prefix="rm_character", choices=Games.get_PCs(game.id))
    return render_template(
        "edit/games/dm.html",
        game=game,
        form_edit=form_edit,
        form_delete=form_delete,
        form_players=form_players,
        form_characters=form_characters,
        error_target=error_target,
    )


def edit_game_details(game, form):
    '''
    Edit the game details
    
    :param game: The SQLAlchemy game object
    :param form: The form object that was submitted
    '''
    game.name = form.name.data if form.name.data else game.name
    game.published = form.published.data
    if form.img.data:
        img_id = Images.upload(form.img.name)
        id_ = game.img_id
        game.img_id = img_id
        Images.query.get(id_).delete_self() if img_id else None


def delete_game_and_assets(g):
    '''
    Delete all the game's assets and then delete the game itself

    :param g: The SQLAlchemy game instance of the game to delete
    '''
    [
        br.delete_self()
        for br in BridgeGameCharacters.query.filter_by(game_id=g.id).all()
    ]
    [br.delete_self() for br in BridgeGamePlaces.query.filter_by(game_id=g.id).all()]
    [br.delete_self() for br in BridgeGameNPCs.query.filter_by(game_id=g.id).all()]
    [br.delete_self() for br in BridgeGameItems.query.filter_by(game_id=g.id).all()]
    [br.delete_self() for br in BridgeUserGames.query.filter_by(game_id=g.id).all()]
    [nt.delete_self() for nt in Notes.query.filter_by(game_id=g.id).all()]
    [se.delete_self() for se in Sessions.query.filter_by(game_id=g.id).all()]
    g.delete_self()


def remove_player(game, form, no_flash=False):
    '''
    Remove a player and their characters from a game 
    
    :param game: The SQLAlchemy game instance of the game the player player is being removed from
    :param form: The form that was submitted
    :param no_flash: If True, don't flash messages, defaults to False (optional)
    '''

    player_to_rm = Users.query.get(form.players.data)
    ptr_pcs = [c for c in player_to_rm.get_character_list_from_game(game.id)]
    bgc = BridgeGameCharacters.query.filter_by(game_id=game.id).all()
    br_ids = set([br.character_id for br in bgc])
    pc_ids = set([c.id for c in ptr_pcs])
    char_ids_to_rm = pc_ids.intersection(br_ids)
    for br in bgc:
        if br.character_id in char_ids_to_rm:
            br.delete_self()
    player = BridgeUserGames.query.filter_by(
        game_id=game.id, user_id=player_to_rm.id
    ).first()
    player.delete_self()
    if not no_flash:
        [flash(f"{c.name} removed from {game.name}") for c in ptr_pcs]
        flash(f"{player_to_rm.name} removed from {game.name}")


def remove_character(game, form):
    '''
    Remove a character from a game
    
    :param game: The SQLAlchemy game instance that the character is being removed from
    :param form: The form object that was submitted
    :param choices: a list of tuples, where each tuple is a character id and the associated character's name
    '''
    char_to_rm = BridgeGameCharacters.query.filter_by(
        game_id=game.id, character_id=form.characters.data
    ).first()
    flash(f"{Characters.query.get(char_to_rm.character_id).name} removed from {game.name}")
    char_to_rm.delete_self()
