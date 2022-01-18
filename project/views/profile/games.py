from flask import render_template


def games_get():
    return render_template("profile/games/landing.html")
