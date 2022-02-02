from flask import render_template
from flask_login import current_user

from project.models import Characters


def characters_get():
    """
    GET request function for "profile/characters.html"

    display user's character information to them
    :return: The template profile/characters.html
    """
    my_characters = Characters.get_list_from_user(current_user.id)
    return render_template("profile/characters.html", my_characters=my_characters)
