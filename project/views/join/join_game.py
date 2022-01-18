from flask import render_template, redirect, url_for
from flask_login import current_user

from project import form_validators
from project.forms.create_character import CharCreate
from project.forms.edit_game_player import CharAdd
from project.models import Games, Users, Images, Characters


def join_game_get(game_id, game_name):
    """Serve new character form to User"""

    charform = CharCreate()
    resources = Joining.make_add_list()
    game = Games.query.get(int(game_id))

    return render_template(
        "joining.html",
        charform=charform,
        addform=resources["addform"],
        my_characters=resources["my_characters"],
        game=game,
    )


def join_game_post(game_id, game_name):
    """add new character to game"""
    game_id = int(game_id)
    addform = CharAdd()
    charform = CharCreate()
    if addform.char_add_submit.data:
        if Joining.handle_add(addform, game_id):
            return Joining._success(game_id)
    elif charform.char_submit.data:
        if Joining.handle_create(charform, game_id):
            return Joining._success(game_id)
    return Joining.failure(game_id, game_name)


class Joining:
    @staticmethod
    def make_add_list():
        form = CharAdd()
        my_characters = Characters.get_list_from_user(current_user.id)
        print(f"my_characters: {my_characters}")
        form.character.choices = [(g.id, g.name) for g in my_characters]
        return {"my_characters": my_characters, "addform": form}

    @staticmethod
    def _failure(game_id, game_name):
        return redirect(url_for("join.joining", game_id=game_id, game_name=game_name))

    @staticmethod
    def _success(game_id):
        return redirect(url_for("notes.game", game_id=game_id))

    @staticmethod
    def add_user(game_id):
        if Users.add_to_game(current_user.id, game_id):
            return True
        return False

    @classmethod
    def handle_add(cls, form, game_id):

        if not form_validators.Character.add(form):
            return False
        if Characters.add_character_to_game(int(form.character.data), game_id):
            if cls.add_user(game_id):
                return True
            cls.rollback_bridge(int(form.character.data), game_id=game_id)
            return False
        return False

    @classmethod
    def handle_create(cls, form, game_id):
        if not form_validators.Character.create(form):
            return False
        img_id = None
        if form.img.data:
            img_id = Images.upload(form.img.name)
            if not img_id:
                return False
        new = Characters.create(
            name=form.name.data,
            bio=form.bio.data,
            user_id=current_user.id,
            img_id=img_id,
        )
        if new:
            if new.add_to_game(game_id):
                if cls.add_user(game_id):
                    return True
                cls.rollback_bridge(character_id=form.character.data, game_id=game_id)
                cls.rollback_character(new.id)
            cls.rollback_character(new.id)
        return False
