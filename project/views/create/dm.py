from flask import redirect, render_template, url_for
from flask_login import current_user

from project.forms.create_dm import DMCreate
from project.models import BridgeGameCharacters, Games, Images, Characters
from project.helpers.db_session import db_session

dm_default_image = "/static/images/default_dm.jpg"


def dm_get(game):
    """
    GET request function for "create/dm.html"

    This function is used to create and customiz a user's DM avatar for a game

    :param game.id: The id of the game that the DM is creating a character for
    :return: The rendered template for the DM creation page.
    """
    form = DMCreate()
    return render_template(
        "create/dm.html", game=game, form=form, dm_default_image=dm_default_image
    )


def dm_post(game):
    """
    POST request function for "create/dm.html"

    Create a DM avatar for a game

    :param game: The SQLAlchemy game object the DM avatar is being created for.
    :return: redirect to the game's notes page
    """
    form = DMCreate()
    if not form.validate_on_submit():
        return render_template(
            "create/dm.html", game=game, form=form, dm_default_image=dm_default_image
        )
    with db_session() as sess:
        img_id = Images.upload(form.img.name) if form.img.data else None
        avatar = Characters.create(
            name=form.name.data, dm=True, user_id=current_user.id, img_id=img_id
        )
        sess.flush()
        BridgeGameCharacters.create(dm=True, character_id=avatar.id, game_id=game.id)
        return redirect(url_for("notes.game", game_id=game.id))
