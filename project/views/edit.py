from flask import Blueprint, render_template, redirect, url_for, session, flash
from flask_login import login_required, fresh_login_required, current_user
from project import forms
from project import form_validators

from project.models import Characters, Users, Games, Images
from project import defaults as d
from project.__init__ import db

edit = Blueprint('edit', __name__)

#######################################
###            Account             ####
#######################################

@edit.route('/edit/account', methods=["GET"])
@fresh_login_required
def account():

    edit_form = forms.UserEdit()
    del_form = forms.UserDelete()
    # form.name.data = current_user.name
    # form.email.data = current_user.email
    # form.password.data = ""
    return render_template('edit/account.html'
                            , user=current_user
                            , edit_form = edit_form
                            , del_form = del_form
                            )

@edit.route('/edit/account', methods=["POST"])
@fresh_login_required
def account_post():

    edit_form = forms.UserCreate()
    del_form = forms.UserDelete()
    if del_form.user_delete_submit.data:
        return redirect(url_for('profile.delete'))
    if not form_validators.User.edit(edit_form):
        return redirect(url_for('edit.account'))
    return redirect(url_for('profile.account'))

#######################################
###            Character           ####
#######################################

@edit.route('/edit/character/<int:character_id>', methods = ['GET'])
@login_required
def character(character_id):
    charform = forms.CharCreate()
    delform = forms.CharDelete()
    character = Characters.get_from_id(character_id)
    charform.bio.data = character.bio
    return render_template("edit/character.html"
                            , charform=charform
                            , character = character
                            , delform = delform
    )

@edit.route('/edit/character/<int:character_id>', methods = ['POST'])
@login_required
def character_post(character_id):
    charform = forms.CharCreate()
    delform = forms.CharDelete()
    character = Characters.get_from_id(character_id)
    if delform.char_del_submit.data:
        confirm = form_validators.Character.remove(delform, character)
        if not confirm:
            return redirect(url_for("edit.character", character_id=character_id))
        character.remove_self()
    elif charform.char_submit.data:
        success = form_validators.Character.create(charform)
        if not success:
            return redirect(url_for("edit.character", character_id=character_id))
        elif success == "no image":
            img_id = character.img_id
        else:
            img_id = Images.upload(success["pic"], success["secure_name"], success["mimetype"]) 
        character.name=charform.name.data
        character.bio = charform.bio.data
        character.img_id = img_id
        db.session.commit()
        # character.edit(name=charform.name.data, bio=charform.bio.data, img_id=img_id)
    return redirect(url_for("profile.characters"))


# #######################################
# ###            DM Game             ####
# #######################################



@edit.route('/edit/games/dm/<int:game_id>', methods = ['GET'])
@login_required
def game_dm(game_id):
    form_edit = forms.GameEdit()
    form_remove = forms.GameRemove()
    form_delete = forms.GameDelete()
    game = Games.get_from_id(game_id)
    print(game)
    # visit game
    # edit game name
    # remove game
    # remove players
    # make someone else game owner
    # claim game if abandoned
    return render_template('edit/games/dm.html'
                            , game = game
                            , form_edit = form_edit
                            , form_remove = form_remove
                            , form_delete = form_delete
                            )

def _game_dm_failure(game_id):
    return redirect(url_for("edit.game_dm", game_id=game_id))

def _game_dm_success(game_id):
    return redirect(url_for("edit.game_dm", game_id=game_id))

def validate_edit(form):
    if form.name.data:
        if not form_validators.Game.name(form.name.data):
            return False
    if form.img.data:
        if not form_validators.Game.image(form.img.name):
            return False
    if type(form.private.data) is not bool:
        flash("Data corrupted")
        return False
    if type(form.published.data) is not bool:
        flash("Data corrupted")
        return False
    return True
def delete_old_image(image_id):
    if image_id:
        image = Images.get_from_id(image_id)
        image.delete_self(confirm=True)
    return

def handle_game_edit(form, game_id):

    if not validate_edit(form):
        return _game_dm_failure(game_id)
    game = Games.get_from_id(game_id)
    if form.img.data:
        img_id = Images.upload(form.img.name)
        old_id = game.img_id
        game.img_id = img_id
    if form.name.data:
        game.name = form.name.data
    if form.published.data:
        game.published = True
    if form.private.data:
        game.published = False
    db.session.commit()
    delete_old_image(old_id)
    return _game_dm_success(game_id)

def handle_game_remove(form):
    return

def handle_game_delete(form):
    return

@edit.route('/edit/games/dm/<int:game_id>', methods = ['POST'])
@login_required
def game_dm_post(game_id):
    form_edit = forms.GameEdit()
    form_remove = forms.GameRemove()
    form_delete = forms.GameDelete()

    if form_edit.game_edit_submit.data:
        handle_game_edit(form_edit, game_id)
    elif form_remove.game_remove_submit.data:
        handle_game_remove(form_remove)
    elif form_delete.game_delete_submit.data:
        handle_game_delete(form_delete)

    # visit game
    # edit game name
    # remove game
    # remove players
    # make someone else game owner
    # claim game if abandoned
    return redirect(url_for('edit.game_dm', game_id=game_id)) 

@edit.route('/edit/games/dm/remove/<int:game_id>', methods = ['GET'])
@login_required
def game_dm_remove_confirm(game_id):
    form = forms.GameRemove()
    form.heir.choices = [(g.id) for g in Users.query.order_by('name')]
    pass

@edit.route('/edit/games/dm/delete/<int:game_id>', methods = ['GET'])
@login_required
def game_dm_delete_confirm(game_id):
    pass