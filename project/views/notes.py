import os
import json

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from project import form_validators, forms
from project.defaults import Character
from project.models import (
    BridgeGameCharacters,
    Games,
    BridgeUserGames,
    Users,
    Images,
    Characters,
    Sessions,
    Notes,
    NPCs,
)
from project import defaults as d
from project.helpers import attach_game_image_or_default_from_Images_model

notes = Blueprint("notes", __name__)


@notes.route("/notes/<int:game_id>", methods=["GET"])
@login_required
def game(game_id):
    tutorial = Users.get_admin()
    game = Games.get_from_id(game_id)
    character_list = get_game_character_list(game)
    session_list = Sessions.get_list_from_gameID(game_id)
    notes = get_game_notes(session_list, game_id)
    js_note_dict = convert_to_JSON(notes)
    heroku = set_heroku()
    return render_template(
        "notes/blueprint.html",
        tutorial=tutorial,
        js_note_dict=js_note_dict,
        edit_img="/static/images/edit_button_image.png",
        note_dict=notes,
        id=game_id,
        bugs_id=d.GameBugs.id,
        session_titles=session_list,
        game=game,
        heroku=heroku,
        character_list=character_list,
    )

def get_game_notes(session_list: list, game_id: int):
    game_notes_by_session = {}
    if session_list is not None:
        for session in session_list:
            session_note_list = Notes.get_list_from_session_number(
                session.number, game_id
            )
            game_notes_by_session[session.number] = session_note_list
    return game_notes_by_session

def set_heroku():
    """this is to set the address for Flask socket.io"""
    heroku = False
    if os.environ.get("HEROKU_HOSTING"):
        heroku = True
    return heroku


def convert_to_JSON(game_notes_by_session) -> dict:
    """convert notes to JSON so that the js script attached to notes.html can insert the rich text.
    This has to be done because otherwise the html won't be able to read the mark up"""

    js_logs = {}
    for session in game_notes_by_session:
        js_logs[session] = []
        for note in game_notes_by_session[session]:
            js_logs[session].append([note.id, note.text])
    return json.dumps(js_logs)


def get_game_character_list(game):
    if current_user.id == game.dm_id:

        character_list = Characters.get_player_list_for_current_user_from_game(game.id)
        if character_list:
            for character in character_list:
                if character.dm is True:
                    choices = character
        npcs = NPCs.get_list(current_user.id)
        for npc in npcs:
            choices.append(npc)
    else:
        character_list = Characters.get_player_list_for_current_user_from_game(game.id)
    choices = [character for character in character_list]
    return choices
