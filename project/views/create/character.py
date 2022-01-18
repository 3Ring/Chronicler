from flask import redirect, render_template, url_for
from flask_login import current_user

from project.forms.create_character import CharCreate
from project.models import Images, Characters
from project.helpers.db_session import db_session


def character_get():
    form = CharCreate()
    return render_template("/create/character.html", form=form)


def character_post():
    form = CharCreate()
    if not form.validate_on_submit():
        return render_template("/create/character.html", form=form)
    with db_session():
        img_id = Images.upload(form.img.name) if form.img.data else None
        Characters.create(
            name=form.name.data,
            bio=form.bio.data,
            user_id=current_user.id,
            img_id=img_id,
        )
        return redirect(url_for("profile.characters"))
