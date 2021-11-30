from flask import Blueprint, redirect, url_for
from flask_login import login_required

from project.models import Users, Games

bugs = Blueprint('bugs', __name__)

@bugs.route("/bugs_page")
@login_required
def bugs_page():

    _bugs = Games.get_bugs()
    if _bugs:
        return redirect(url_for("notes.game", game_id=25))
    