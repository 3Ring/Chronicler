from flask import render_template, redirect, url_for

from project.__init__ import db
from project.helpers.db_session import db_session
from project.models import Users, Characters, Games
from project.forms.register import Register


def register_get():
    """direct user to registration page"""
    form = Register()
    return render_template("register.html", form=form)


def register_post():
    """register new users"""
    form = Register()
    if not form.validate_on_submit():
        return render_template("register.html", form=form)
    with db_session():
        user = Users.create(
            name=form.name.data, email=form.email.data, password=form.password.data
        )
        db.session.flush()
        avatar = Characters.create(name=user.name, user_id=user.id, avatar=True)
        avatar.add_to_game(Games.get_bugs().id)
    return redirect(url_for("auth.login"))
