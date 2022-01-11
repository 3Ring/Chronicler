from flask import Blueprint
from flask_login import fresh_login_required


edit = Blueprint("edit", __name__)


@edit.route("/edit/account", methods=["GET"])
@fresh_login_required
def account():
    from project.views.edit_pages.account import get

    return get()


@edit.route("/edit/account", methods=["POST"])
@fresh_login_required
def account_post():
    from project.views.edit_pages.account import post

    return post()


@edit.route("/edit/account/delete", methods=["GET"])
@fresh_login_required
def delete_get():
    from project.views.edit_pages.account import confirm_get

    return confirm_get()


@edit.route("/edit/account/delete", methods=["POST"])
@fresh_login_required
def delete_post():
    from project.views.edit_pages.account import confirm_post

    return confirm_post()


@edit.route("/edit/character/<int:character_id>", methods=["GET"])
@fresh_login_required
def character(character_id):
    from project.views.edit_pages.character import get

    return get(character_id)


@edit.route("/edit/character/<int:character_id>", methods=["POST"])
@fresh_login_required
def character_post(character_id):

    from project.views.edit_pages.character import post

    return post(character_id)


@edit.route("/edit/games/dm/<int:game_id>", methods=["GET"])
@fresh_login_required
def game_dm(game_id):
    from project.views.edit_pages.game_dm import get

    return get(game_id)


@edit.route("/edit/games/dm/<int:game_id>", methods=["POST"])
@fresh_login_required
def game_dm_post(game_id):
    from project.views.edit_pages.game_dm import post

    return post(game_id)


@edit.route("/edit/games/player/add_remove/<int:game_id>", methods=["GET"])
@fresh_login_required
def add_remove(game_id):
    from project.views.edit_pages.game_player import get

    return get(game_id)


@edit.route("/edit/games/player/add_remove/<int:game_id>", methods=["POST"])
@fresh_login_required
def add_remove_post(game_id):
    from project.views.edit_pages.game_player import post

    return post(game_id)


@edit.route("/edit/games/player/leave/<int:game_id>", methods=["GET"])
@fresh_login_required
def leave(game_id):
    from project.views.edit_pages.game_player import leave_get

    return leave_get(game_id)


@edit.route("/edit/games/player/leave/<int:game_id>", methods=["POST"])
@fresh_login_required
def leave_post(game_id):
    from project.views.edit_pages.game_player import leave_post_

    return leave_post_(game_id)
