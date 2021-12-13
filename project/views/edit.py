from os import fstat
from flask import Blueprint, render_template, redirect, url_for, session, flash
from flask_login import login_required, fresh_login_required, current_user
from project import forms
from project import form_validators

from project.models import (
    BridgeGameCharacters,
    BridgeUserGames,
    Characters,
    Users,
    Games,
    Images,
    ViewsMixin,
)
from project import defaults as d
from project.__init__ import db

edit = Blueprint("edit", __name__)

#######################################
###            Account             ####
#######################################


@edit.route("/edit/account", methods=["GET"])
@fresh_login_required
def account():

    edit_form = forms.UserEdit()
    del_form = forms.UserDelete()
    # form.name.data = current_user.name
    # form.email.data = current_user.email
    # form.password.data = ""
    return render_template(
        "edit/account.html", user=current_user, edit_form=edit_form, del_form=del_form
    )


@edit.route("/edit/account", methods=["POST"])
@fresh_login_required
def account_post():

    edit_form = forms.UserCreate()
    del_form = forms.UserDelete()
    if del_form.user_delete_submit.data:
        return redirect(url_for("profile.delete"))
    if not form_validators.User.edit(edit_form):
        return redirect(url_for("edit.account"))
    return redirect(url_for("profile.account"))


#######################################
###            Character           ####
#######################################


@edit.route("/edit/character/<int:character_id>", methods=["GET"])
@fresh_login_required
def character(character_id):
    charform = forms.CharCreate()
    delform = forms.CharDelete()
    character = Characters.get_from_id(character_id)
    charform.bio.data = character.bio
    return render_template(
        "edit/character.html", charform=charform, character=character, delform=delform
    )


@edit.route("/edit/character/<int:character_id>", methods=["POST"])
@fresh_login_required
def character_post(character_id):

    charform = forms.CharCreate()
    delform = forms.CharDelete()
    character = Characters.get_from_id(character_id)
    if delform.char_del_submit.data:
        confirm = form_validators.Character.remove(delform, character)
        if not confirm:
            return redirect(url_for("edit.character", character_id=character_id))
        character.remove_self()
    elif charform.char_submit.data:
        success = form_validators.Character.create(charform)
        if not success:
            return redirect(url_for("edit.character", character_id=character_id))
        elif success == "no image":
            img_id = character.img_id
        else:
            img_id = Images.upload(
                success["pic"], success["secure_name"], success["mimetype"]
            )
        character.name = charform.name.data
        character.bio = charform.bio.data
        character.img_id = img_id
        db.session.commit()
        # character.edit(name=charform.name.data, bio=charform.bio.data, img_id=img_id)
    return redirect(url_for("profile.characters"))


#######################################
###            DM Game             ####
#######################################


no_choice = "No Choice"


@edit.route("/edit/games/dm/<int:game_id>", methods=["GET"])
@fresh_login_required
def game_dm(game_id):
    if DM.not_authorized(game_id):
        return redirect(url_for(DM.not_authorized_url))
    heir = False
    form_edit = forms.GameEdit()
    form_remove = forms.GameRemove()
    form_delete = forms.GameDelete()
    game = Games.get_from_id(game_id)
    player_list = Users.get_player_list(game_id)
    form_remove.heir.choices = [no_choice]
    for i, player in enumerate(player_list):
        if player.id != current_user.id:
            form_remove.heir.choices.append(player.name)
            form_remove.heir.choices[i + 1].value = player.id

    if len(form_remove.heir.choices) > 1:
        heir = True
    # visit game
    # edit game name
    # remove game
    # remove players
    # make someone else game owner
    # claim game if abandoned
    return render_template(
        "edit/games/dm.html",
        game=game,
        heir=heir,
        form_edit=form_edit,
        form_remove=form_remove,
        form_delete=form_delete,
    )


@edit.route("/edit/games/dm/<int:game_id>", methods=["POST"])
@fresh_login_required
def game_dm_post(game_id):
    form_edit = forms.GameEdit()
    form_remove = forms.GameRemove()
    form_delete = forms.GameDelete()

    if form_edit.game_edit_submit.data:
        GameDM.handle_edit(form_edit, game_id)
    elif form_remove.game_remove_submit.data:
        GameDM.handle_remove(form_remove)
    elif form_delete.game_delete_submit.data:
        GameDM.handle_delete(form_delete)

    # visit game
    # edit game name
    # remove game
    # remove players
    # make someone else game owner
    # claim game if abandoned
    return redirect(url_for("edit.game_dm", game_id=game_id))


@edit.route("/edit/games/dm/remove/<int:game_id>", methods=["GET"])
@fresh_login_required
def game_dm_remove_confirm(game_id):
    form = forms.GameRemove()
    form.heir.choices = [(g.id) for g in Users.query.order_by("name").all()]
    pass


@edit.route("/edit/games/dm/delete/<int:game_id>", methods=["GET"])
@fresh_login_required
def game_dm_delete_confirm(game_id):
    pass


class GameDM(ViewsMixin):
    @staticmethod
    def _failure(game_id):
        return redirect(url_for("edit.game_dm", game_id=game_id))

    @staticmethod
    def _success(game_id):
        return redirect(url_for("edit.game_dm", game_id=game_id))

    @staticmethod
    def validate_edit(form):
        if form.name.data:
            if not form_validators.Game.name(form.name.data):
                return False
        if form.img.data:
            if not form_validators.Game.image(form.img.name):
                return False
        if type(form.private.data) is not bool:
            flash("Data corrupted")
            return False
        if type(form.published.data) is not bool:
            flash("Data corrupted")
            return False
        return True

    @staticmethod
    def delete_old_image(image_id):
        if image_id:
            image = Images.get_from_id(image_id)
            image.delete_self(confirm=True)
        return

    @classmethod
    def handle_edit(cls, form, game_id):

        if not cls.validate_edit(form):
            return cls._failure(game_id)
        game = Games.get_from_id(game_id)
        if form.img.data:
            img_id = Images.upload(form.img.name)
            old_id = game.img_id
            game.img_id = img_id
        if form.name.data:
            game.name = form.name.data
        if form.published.data:
            game.published = True
        if form.private.data:
            game.published = False
        db.session.commit()
        cls.delete_old_image(old_id)
        return cls._success(game_id)

    @staticmethod
    def handle_remove(form, game_id):
        game = Games.get_from_id(game_id)
        if form.heir.data != no_choice:
            return
        return

    @staticmethod
    def handle_delete(form):
        return


#######################################
###          Player Game           ####
#######################################

from project.views.join import Joining


@edit.route("/edit/games/player/add_remove/<int:game_id>", methods=["GET"])
@fresh_login_required
def add_remove(game_id):

    if Player.not_authorized(game_id):
        return redirect(url_for(Player.not_authorized))
    game = Games.get_from_id(game_id)
    charform = forms.CharCreate()
    resources = Player.get_resources(game_id)
    game_characters = Games.get_personal_game_list_player(current_user.id)
    last_character = False
    if len(resources["remove"]) == 1:
        last_character = resources["remove"][0]

    return render_template(
        "edit/games/add_remove.html",
        game=game,
        addform=resources["addform"],
        my_characters=resources["my_characters"],
        game_characters=game_characters,
        charform=charform,
        removeform=resources["removeform"],
        last_character=last_character,
    )


def manage_remove_character(game, character_id):
    if not Games.remove_character_from_id(character_id):
        return Player.failure(f"unable to remove character from {game.name}")
    name = Characters.get_from_id(character_id).name
    return Player.success(game.id, f"{name} removed from {game.name} successfully")


@edit.route("/edit/games/player/add_remove/<int:game_id>", methods=["POST"])
@fresh_login_required
def add_remove_post(game_id):
    if Player.not_authorized(game_id):
        return redirect(url_for(Player.not_authorized))
    game = Games.get_from_id(game_id)
    addform = forms.CharAdd()
    charform = forms.CharCreate()
    delform = forms.CharRemove()
    if addform.char_add_submit.data:
        message = Joining.handle_add(addform, game_id)
        if type(message) is not str:
            return Player.success(
                game_id, f"{addform.character.name} successfully added to {game.name}"
            )
        return Player.failure(game_id, message)
    elif charform.char_submit.data:
        message = Joining.handle_create(charform, game_id)
        if type(message) is not str:
            return Player.success(
                game_id, f"{addform.character.name} successfully added to {game.name}"
            )
    else:
        return manage_remove_character(game, delform.character.data)


@edit.route("/edit/games/player/leave/<int:game_id>", methods=["GET"])
@fresh_login_required
def leave(game_id):
    if Player.not_authorized(game_id):
        return redirect(url_for(Player.not_authorized))
    game = Games.get_from_id(game_id)
    leaveform = forms.LeaveGame()
    return render_template("edit/games/leave.html", game=game, leaveform=leaveform)


@edit.route("/edit/games/player/leave/<int:game_id>", methods=["POST"])
@fresh_login_required
def leave_post(game_id):
    if Player.not_authorized(game_id):
        return redirect(url_for(Player.not_authorized))
    leaveform = forms.LeaveGame()
    return handle_leave(game_id, leaveform)


def handle_leave(game_id, form):
    message = form_validators.Game.leave(form)
    if type(message) is str:
        return Player.leave_failure(game_id, message)
    game_name = Games.get_from_id(game_id).name.lower().strip()
    confirm = form.confirm.data.lower().strip()
    if confirm != game_name:
        return Player.leave_failure(game_id, f"{confirm} does not match {game_name}")
    Games.remove_player(current_user.id, game_id)
    return Player.leave_success(game_id, f"You are no longer part of {game_name}")


class DM(ViewsMixin):
    not_authorized_url = "profile.dm"

    @staticmethod
    def not_authorized(game_id):
        dm_id = Games.get_dmID_from_gameID(game_id)
        if current_user.id == dm_id:
            return False
        return True


class Player(ViewsMixin):

    not_authorized_url = "profile.player"

    @staticmethod
    def success(game_id, message=None):
        if message:
            flash(message)
        return redirect(url_for("edit.add_remove", game_id=game_id))

    @staticmethod
    def failure(game_id, message=None):
        if message:
            flash(message)
        return redirect(url_for("edit.add_remove", game_id=game_id))

    @staticmethod
    def leave_success(game_id, message=None):
        if message:
            flash(message)
        return redirect(url_for("profile.player", game_id=game_id))

    @staticmethod
    def leave_failure(game_id, message=None):
        if message:
            flash(message)
        return redirect(url_for("edit.leave", game_id=game_id))

    @staticmethod
    def not_authorized(game_id):
        user_list = Games.get_player_list_from_id(game_id)
        for user in user_list:
            if current_user.id == user.id:
                return False
        return True

    @staticmethod
    def get_resources(game_id):

        addform = forms.CharAdd()
        removeform = forms.CharRemove()
        add = []
        ids = []

        remove_list = Characters.get_player_list_for_current_user_from_game(game_id)
        add_list = Characters.get_list_from_user(current_user.id)
        for player in remove_list:
            ids.append(player.id)
        for character in add_list:
            if character.id not in ids:
                add.append(character)
        addform.character.choices = [(g.id, g.name) for g in add]
        removeform.character.choices = [(g.id, g.name) for g in remove_list]
        return {
            "my_characters": add,
            "removeform": removeform,
            "addform": addform,
            "remove": remove_list,
        }
