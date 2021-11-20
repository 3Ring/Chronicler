from flask import Blueprint, redirect
from flask_login import login_required

from project.models import Users, Games

bugs = Blueprint('bugs', __name__)

@bugs.route("/bug_page")
@login_required
def bug_page():

    game = Games.query_from_id(-1)
    if game:
        return redirect("main.notes", game_id=-1)
    admin = Users.get_admin()
    Games.create(id=-1, name="Bugs and suggestions", dm_id=admin.id)
    
    