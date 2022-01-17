
from flask import render_template, redirect, url_for, flash
from project import forms
from project import form_validators

from project.models import Characters, Images
from project.helpers.db_session import db_session
from project.__init__ import db

def get(character_id):
    charform = forms.CharCreate()
    delform = forms.CharDelete()
    character = Characters.query.get(character_id)
    charform.bio.data = character.bio
    return render_template(
        "edit/character.html", charform=charform, character=character, delform=delform
    )

def post(character_id):

    charform = forms.CharCreate()
    delform = forms.CharDelete()
    with db_session():
        character = Characters.query.get(character_id)
        if delform.char_del_submit.data:
            confirm = form_validators.Character.remove(delform, character)
            if not confirm:
                return redirect(url_for("edit.character", character_id=character_id))
            character.removed = True
        elif charform.char_submit.data:
            if charform.img.data:
                img_id = Images.upload(charform.img.name)
                character.img_id = img_id
            if charform.name.data:
                if charform.validate():
                    character.name = charform.name.data
            if charform.bio.data:
                character.bio = charform.bio.data
    return redirect(url_for("profile.characters"))