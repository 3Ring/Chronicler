from flask import redirect, render_template, url_for
from flask_login import current_user

from project.forms.create_character import CharCreate
from project.models import Images, Characters
from project.helpers.db_session import db_session


def character_get():
    '''
    GET request function for "/create/character.html"

    This function renders the character creation page
    :return: The rendered creation page template.
    '''
    form = CharCreate()
    return render_template("/create/character.html", form=form)


def character_post():
    '''
    POST request function for "/create/character.html"

    This function creates a character using the form data from the character creation page
    :return: A redirect to the user's characters page.
    '''
    form = CharCreate()
    if not form.validate_on_submit():
        return render_template("/create/character.html", form=form)
    with db_session():
        create_character(form)
        return redirect(url_for("profile.characters"))

def create_character(form):
    '''
    Create a character and add to database with the given form data

    this is split off because it is used in other view functions
    :param form: The form object that was submitted
    '''
    img_id = Images.upload(form.img.name) if form.img.data else None
    Characters.create(
        name=form.name.data,
        bio=form.bio.data,
        user_id=current_user.id,
        img_id=img_id,
    )