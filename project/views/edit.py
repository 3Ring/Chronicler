from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from project import forms

from project.models import Users, Games


edit = Blueprint('edit', __name__)

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

def handle_game_edit(form):
    print("edit")
    if form.name.data:
        pass
    return

def handle_game_remove(form):
    print("remove")
    return

def handle_game_delete(form):
    print("delete")
    return

@edit.route('/edit/games/dm/<int:game_id>', methods = ['POST'])
@login_required
def game_dm_post(game_id):
    form_edit = forms.GameEdit()
    form_remove = forms.GameRemove()
    form_delete = forms.GameDelete()

    if form_edit.game_edit_submit.data:
        handle_game_edit(form_edit)
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