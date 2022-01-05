
from flask import render_template, redirect, url_for
from project import forms
from project import form_validators

from project.models import Characters, Images

from project.__init__ import db

def get(character_id):
    charform = forms.CharCreate()
    delform = forms.CharDelete()
    character = Characters.get_from_id(character_id)
    charform.bio.data = character.bio
    return render_template(
        "edit/character.html", charform=charform, character=character, delform=delform
    )

def post(character_id):
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
            img_id = Images.upload(
                success["pic"], success["secure_name"], success["mimetype"]
            )
        character.name = charform.name.data
        character.bio = charform.bio.data
        character.img_id = img_id
        db.session.commit()
        # character.edit(name=charform.name.data, bio=charform.bio.data, img_id=img_id)
    return redirect(url_for("profile.characters"))