from flask import redirect, render_template, url_for
from flask_login import current_user

from project.forms.create_game import GameCreate
from project.models import Games, Images, BridgeUserGames
from project.helpers.db_session import db_session

def game_get():
    form = GameCreate()
    return render_template("create/game.html", gameform=form)


def game_post():
    form = GameCreate()
    if not form.validate_on_submit():
        return render_template("create/game.html", gameform=form)
    with db_session() as sess:
        img_id = Images.upload(form.img.name) if form.img.data else None
        game = Games.create(
            name=form.name.data,
            dm_id=current_user.id,
            published=form.published.data,
            img_id=img_id
        )
        Games.new_game_training_wheels(game)
        sess.flush()
        BridgeUserGames.create(owner=True, user_id=game.dm_id, game_id=game.id)
        return redirect(url_for("create.dm", game_id=game.id))
