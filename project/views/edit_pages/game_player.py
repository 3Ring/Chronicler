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
    
)
from project.helpers import set_heroku
from project import defaults as d
from project.__init__ import db

def get(game_id):
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

def post(game_id):
    from project.views.join import Joining
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

def manage_remove_character(game, character_id):
    if not Games.remove_character_from_id(character_id):
        return Player.failure(f"unable to remove character from {game.name}")
    name = Characters.get_from_id(character_id).name
    return Player.success(game.id, f"{name} removed from {game.name} successfully")


def leave_get(game_id):
    if Player.not_authorized(game_id):
        return redirect(url_for(Player.not_authorized))
    game = Games.get_from_id(game_id)
    leaveform = forms.LeaveGame()
    return render_template("edit/games/leave.html", game=game, leaveform=leaveform)

def leave_post_(game_id):
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


class Player():

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

        remove_list = Characters.get_player_character_list_for_game(game_id)
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
