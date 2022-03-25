from flask import render_template, redirect, url_for

from project.extensions.sql_alchemy import db
from project.helpers.db_session import db_session
from project.models import Users, Characters, Games
from project.forms.register import Register


def register_get():
    """
    GET request function for "auth/register.html"

    A page to register new users.
    :return: A rendered template with a form.
    """
    print("get")
    form = Register()
    return render_template("auth/register.html", form=form)


def register_post():
    """
    POST request function for "auth/register.html"

    Create a new user and add them to the database
    :return: Redirect to the login page.
    """
    
    from flask import request
    print(f'request: {request.get_data()}')
    form = Register()
    if not form.validate_on_submit():
        return render_template("auth/register.html", form=form)
    with db_session():
        user = Users.create(
            name=form.name.data, email=form.email.data, password=form.password.data
        )
        db.session.flush()
        avatar = Characters.create(name=user.name, user_id=user.id, avatar=True)
        avatar.add_to_game(Games.get_bugs().id)
    return redirect(url_for("auth.login"))
