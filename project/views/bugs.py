from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required

from project.models import Users, Games, Sessions, Notes
from project import defaults as d
from project.views.notes import set_heroku, get_game_notes, convert_to_JSON
bugs = Blueprint("bugs", __name__)


@bugs.route("/bugs", methods=["GET"])
@login_required
def bugs_page():
    tutorial = Users.get_admin()
    game = Games.get_bugs()
    heroku = set_heroku()
    session_list = Sessions.get_list_from_gameID(d.GameBugs.id)
    notes = get_game_notes(session_list, d.GameBugs.id)
    js_note_dict = convert_to_JSON(notes)

    return render_template(
        "notes/blueprint.html",
        tutorial=tutorial,
        js_note_dict=js_note_dict,
        edit_img="/static/images/edit_button_image.png",
        note_dict=notes,
        id=d.GameBugs.id,
        bugs_id=d.GameBugs.id,
        session_titles=session_list,
        game=game,
        heroku=heroku,
    )

    # _bugs = Games.get_bugs()
    # if _bugs:
    #     return redirect(url_for("notes.game", game_id=_bugs.id))
