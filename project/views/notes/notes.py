import json

from flask import render_template
from flask_login import current_user

from project.helpers.misc import set_heroku

from project.models import (
    Games,
    Users,
    Characters,
    Sessions,
    Notes,
    NPCs,
)
from project.setup_ import defaults as d


def notes_get(game_id):
    tutorial = Users.get_admin()
    game = Games.query.get(game_id)
    character_list = get_game_character_list(game)
    session_list = Sessions.get_list_from_gameID(game_id)
    notes = get_game_notes(session_list, game_id)
    js_note_dict = convert_to_JSON(notes)
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
        heroku=set_heroku(),
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

        character_list = Characters.get_player_character_list_for_game(game.id)
        if character_list:
            for character in character_list:
                if character.dm is True:
                    choices = character
        npcs = NPCs.get_list(current_user.id)
        for npc in npcs:
            choices.append(npc)
    else:
        character_list = Characters.get_player_character_list_for_game(game.id)
    choices = [character for character in character_list]
    return choices
