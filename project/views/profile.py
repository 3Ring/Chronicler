from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from project.models import Characters, Users, Games


profile = Blueprint('profile', __name__)

@profile.route('/profile')
@login_required
def dashboard():
    user = Users.get_from_id(current_user.id)
    return render_template('profile/dashboard.html'
        , user=user
    )

@profile.route('/profile/account')
@login_required
def account():
    return render_template('profile/account.html')

@profile.route('/profile/characters')
@login_required
def characters():
    my_characters = Characters.get_list_from_userID(current_user.id)
    print(my_characters)
    if not my_characters:
        return redirect(url_for("create.character"))
    return render_template('profile/characters.html'
                            , my_characters = my_characters
                            )

@profile.route('/profile/games')
@login_required
def games():
    return render_template('profile/games/landing.html')

@profile.route('/profile/games/player')
@login_required
def player():

    # claim game if abandoned
    return render_template('profile/games/player.html')

@profile.route('/profile/games/dm')
@login_required
def dm():
    # see list of games
    dm_games = Games.get_personal_game_list_dm(current_user.id)
    return render_template('profile/games/dm.html'
                            , dm_games = dm_games
                            )


