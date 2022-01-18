from flask import render_template, redirect, url_for
from project.forms.edit_character import CharCreate, CharDelete
from project import form_validators

from project.models import Characters, Images
from project.helpers.db_session import db_session


def character_get(character_id):
    charform = CharCreate()
    delform = CharDelete()
    character = Characters.query.get(character_id)
    charform.bio.data = character.bio
    return render_template(
        "edit/character.html", charform=charform, character=character, delform=delform
    )


def character_post(character_id):

    charform = CharCreate()
    delform = CharDelete()
    with db_session():
        if delform.char_del_submit.data:
            delete_character(character_id, charform)
        elif charform.char_submit.data:
            edit_character(character_id, delform)
    return redirect(url_for("profile.characters"))


def delete_character(character_id, form):
    character = Characters.query.get(character_id)
    confirm = form_validators.Character.remove(form, character)
    if not confirm:
        return redirect(url_for("edit.character", character_id=character_id))
    character.removed = True


def edit_character(character_id, form):
    character = Characters.query.get(character_id)
    if form.img.data:
        img_id = Images.upload(form.img.name)
        character.img_id = img_id
    if form.name.data:
        if form.validate():
            character.name = form.name.data
    if form.bio.data:
        character.bio = form.bio.data
