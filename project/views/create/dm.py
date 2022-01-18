from flask import redirect, render_template, url_for, request
from flask_login import current_user

from project import form_validators
from project.forms.create_dm import DMCreate
from project.models import (
    BridgeGameCharacters,
    Games,
    Images,
    Characters,
)
from project.helpers.db_session import db_session


def dm_get(game_id):
    game = Games.query.get(game_id)
    form = DMCreate()
    dm_default_image = "/static/images/default_dm.jpg"
    return render_template(
        "create/dm.html", game=game, form=form, dm_default_image=dm_default_image
    )


def dm_post(game_id):
    form = DMCreate()
    if not form_validators.Character.dm_create(form):
        return redirect(url_for("create.dm", game_id=game_id))
    with db_session():
        img_id = Images.upload(form.img.name) if form.img.data else None
        avatar = Characters.create(
            name=form.name.data, dm=True, user_id=current_user.id, img_id=img_id
        )
        BridgeGameCharacters.create(dm=True, character_id=avatar.id, game_id=game_id)
    return redirect(url_for("notes.game", game_id=game_id))
