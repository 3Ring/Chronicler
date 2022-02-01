from flask import render_template, redirect, url_for
from flask_login import current_user

from project.models import Characters


def characters_get():
    my_characters = Characters.get_list_from_user(current_user.id)
    return render_template("profile/characters.html", my_characters=my_characters)
