from flask import render_template, redirect, url_for, flash
from project.forms.edit_character import CharEdit, CharDelete

from project.models import Images
from project.helpers.db_session import db_session


def character_get(character):
    '''
    Render the character edit page.
    
    :param character: the character to be edited
    :return: The character page.
    '''
    return render_template(
        "edit/character.html",
        editform=CharEdit(prefix="a"),
        character=character,
        delform=CharDelete(prefix="b", char_name=character.name),
    )


def character_post(character):
    '''
    If the form is submitted, update the character's information.
    
    :param character: The character to edit
    :return: A redirect to the profile page.
    '''
    editform = CharEdit(prefix="a")
    delform = CharDelete(prefix="b", char_name=character.name)
    with db_session():
        if delform.submit.data:
            if delform.validate():
                flash(f"{character.name} deleted successfully.")
                character.removed = True
            else:
                return render_template(
                    "edit/character.html",
                    editform=editform,
                    character=character,
                    delform=delform,
                )
        elif editform.submit.data:
            if editform.validate():
                character.img_id = (
                    Images.upload(editform.img.name)
                    if editform.img.data
                    else character.img_id
                )
                character.name = (
                    editform.name.data if editform.name.data else character.name
                )
                character.bio = editform.bio.data if editform.bio.data else character.bio
            else:
                return render_template(
                    "edit/character.html",
                    editform=editform,
                    character=character,
                    delform=delform,
                )
    return redirect(url_for("profile.characters"))
