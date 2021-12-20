from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_login import current_user

from project.models import *
from project import forms

admin = Blueprint("admin", __name__)


def find_claimed_characters():
    # get full player list
    full_player_list = BridgeUserGames.query.all()
    # get list of characters in bridge
    bridge_list = BridgeGameCharacters.query.all()
    added = {}
    for bridge in bridge_list:
        for player in full_player_list:
            if player.game_id == bridge.game_id:
                added[player.id] = bridge.character_id
    return added


@admin.route("/dashboard")
@login_required
def dashboard():
    if current_user.id != Users.get_admin().id:
        return redirect("main.index")
    return render_template("admin_dashboard.html")


@admin.route("/remove_gameid")
@login_required
def remove_gameid():
    chars = Characters.query.all()
    if len(chars) > 0:

        for i, char in enumerate(chars):

            if "game_id" in char.__table__.columns:
                if char.game_id == -2:

                    continue
                test = BridgeGameCharacters.query.filter_by(
                    game_id=char.game_id, character_id=char.id
                ).first()
                if test:

                    continue
                done = BridgeGameCharacters.create(
                    game_id=char.game_id, character_id=char.id
                )

    flash("remove_game_id done")
    return redirect("admin.dashboard")


"""empty message

Revision ID: ce267715952f
Revises: 83616baa15f1
Create Date: 2021-11-23 16:54:31.093542

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ce267715952f"
down_revision = "83616baa15f1"
branch_labels = None
depends_on = None


# if current_user.id != Users.get_admin().id:
#     return redirect(url_for("main.index"))

# full_player_list = Players.query.all()
# final_claimed = []

# for i, player in enumerate(full_player_list):
#     try:
#         _ = claimed[player.id]
#         final_claimed.append(BridgeCharacters.query.filter_by(character_id=claimed[player.id]).first())
#         full_player_list[i] = None
#     except:
#         pass
# final_final = []
# character_final = []
# for player in full_player_list:
#     if not player:
#         continue
#     character_final.append(Characters.query.filter_by(game_id=player.game_id, user_id=player.user_id).first())

# characters = Characters.query.all()
# for bridge in final_claimed:
#     final_final.append(Characters.get_from_id(bridge.character_id))


# email = Users.get_from_email("app@chronicler.gg")

# email.delete_self(confirm=True, orphan=False)
# admin.email = "app@chronicler.gg"
# db.session.commit()



# if first_char:
#     d, i = True, 1
#     while d:
#         char = Characters.get_from_id(i)
#         if not char:
# placeholder = Characters.create(id = i, name = 'placeholder', user_id= 1, game_id = 1)
# notes = Notes.query.filter_by(origin_character_id = 1).all()
# for note in notes:
#     note.origin_character_id = i

#     db.session.commit()
# bridge1 = BridgeCharacters.query.filter_by(character_id= 1).all()
# for item in bridge1:
#     item.character_id= i

#     db.session.commit()
# placeholder = Characters.query.filter_by(name='placeholder').first()
# placeholder.delete_self(confirm=True)


#     first_char.id = i
#     db.session.commit()
#     d = False
# i += 1
# Characters.create(id = 1, name = "Chronicler Helper", user_id = 1, game_id=1)
# first_char = Characters.get_from_id(1)

# delete = Users.get_from_id(-1)
# # delete.delete_self(confirm=True)
# # Users.create(id = -1, name = 'Chronicler Helper', email="app@chronicler.com", password="password123")
# delete.name = "Chronicler Helper"
# delete.email = "app@chronicler.com"
# delete.change_pw("password123")

# first_game = Games.get_from_id(1)


# first_game.move_self(name=first_game.name
#                     , secret = first_game.secret
#                     , published = first_game.published
#                     , date_added = first_game.date_added
#                     , dm_id = first_game.dm_id
#                     , img_id = first_game.img_id\
#                     , image_object = first_game.image_object
#                     , image = first_game.image
#                     )




# delete = Games.get_from_id(88)

# delete.delete_self(confirm = True)

# all_games = Games.query.all()
# all_characters = Characters.query.all()

# first = Games.get_from_id(1)
# def move_game_id(current_id):
#     pass
#     # dependencies
#     bc = BridgeCharacters.query.filter_by(game_id = current_id).all()
#     notes = Notes
# new_place = Characters.get_from_id(i)



# helpers = Characters.query.filter_by(name="Chronicler Helper").all()

# helper.delete_self(confirm = True)

# , final_claimed = all_games
# )
