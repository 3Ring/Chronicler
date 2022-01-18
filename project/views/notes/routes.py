from flask import Blueprint
from flask_login import login_required

from project.views.notes.notes import notes_get

notes = Blueprint("notes", __name__)


@notes.route("/notes/<int:game_id>", methods=["GET"])
@login_required
def game(game_id):
    return notes_get(game_id)
