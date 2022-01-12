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
    if DM.not_authorized(game_id):
        return redirect(url_for(DM.not_authorized_url))
    game = Games.get_from_id(game_id)
    form_edit = forms.GameEdit()
    form_transfer = forms.GameTransfer()
    form_delete = forms.GameDelete()
    form_players = forms.GameManagePlayers()
    form_characters = forms.GameManageCharacters()
    form_end = forms.GameEnd()
    p_list = Users.get_player_list(game_id)
    for i, p in enumerate(p_list):
        if p.id < 0 or p.id == current_user.id:
            p_list.pop(i)
    form_transfer.heir.choices = form_players.players.choices = [
        (p.id, p.name) for p in p_list
    ]
    players = True if p_list else False
    heir = True if len(form_transfer.heir.choices) > 0 else False
    if p_list:
        characters = []
        for p in p_list:
            char_list = p.get_character_list_from_game(game.id)
            for c in char_list:
                characters.append((c.id, f"{p.name}: {c.name}"))
        form_characters.characters.choices = [(c[0], c[1]) for c in characters]
    return render_template(
        "edit/games/dm.html",
        game=game,
        players=players,
        heir=heir,
        form_edit=form_edit,
        form_transfer=form_transfer,
        form_delete=form_delete,
        form_players=form_players,
        form_characters=form_characters,
        form_end=form_end,
        heroku=set_heroku(),
    )

def post(game_id):
    
    form_edit = forms.GameEdit()
    form_transfer = forms.GameTransfer()
    form_delete = forms.GameDelete()
    form_players = forms.GameManagePlayers()
    form_characters = forms.GameManageCharacters()

    if form_edit.edit_submit.data:
        
        GameDM.handle_edit(form_edit, game_id)
    elif form_transfer.transfer_confirm.data:
        
        GameDM.handle_transfer(form_transfer)
    elif form_delete.game_delete_submit.data:
        
        GameDM.handle_delete(form_delete)
    elif form_players.player_submit.data:
        
        user = Users.get_from_id(form_players.player_id.data)
        pc_list = user.get_character_list_from_game(game_id)
        pc_ids = [p.id for p in pc_list]

        characters = BridgeGameCharacters.query.filter_by(game_id=game_id).all()
        [x.delete_self(confirm=True) for x in characters if x.character_id in pc_ids]
        test_characters = user.get_character_list_from_game(game_id)
        
        player = BridgeUserGames.query.filter_by(
            game_id=game_id, user_id=user.id
        ).first()
        player.delete_self(confirm=True) if player else flash("unable to remove player")
        test_player = BridgeUserGames.query.filter_by(
            game_id=game_id, user_id=user.id
        ).first()
        

    elif form_characters.character_submit.data:
        c = BridgeGameCharacters.query.filter_by(
            game_id=game_id, character_id=form_characters.character_id.data
        ).first()
        c.delete_self(confirm=True) if c else flash("unable to remove character")
    return redirect(url_for("edit.game_dm", game_id=game_id))


class GameDM():
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
    def player_remove(cls, form):

        pass

    @classmethod
    def handle_edit(cls, form, game_id):

        if not cls.validate_edit(form):
            return cls._failure(game_id)
        game = Games.get_from_id(game_id)
        img_id = game.img_id
        name = game.name
        if form.img.data:
            img_id = Images.upload(form.img.name)
            old_id = game.img_id
            cls.delete_old_image(old_id)
        if form.name.data:
            name = form.name.data
        print(img_id, name, form.published.data)
        game.update(img_id=img_id, name=name, published=form.published.data)

        return cls._success(game_id)

    @staticmethod
    def handle_transfer(form, game_id):
        game = Games.get_from_id(game_id)
        if form.heir.data != 'no_choice':
            return
        return

    @staticmethod
    def handle_delete(form):
        return