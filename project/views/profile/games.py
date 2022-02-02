from flask import render_template


def games_get():
    """
    GET request function for "profile/games/landing.html"

    This function returns the landing page for the games section of the profile
    :return: A rendered template.
    """
    return render_template("profile/games/landing.html")
