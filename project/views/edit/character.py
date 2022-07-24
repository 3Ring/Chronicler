from flask import render_template, redirect, url_for, flash
from project.forms.edit_character import CharEdit, CharDelete

from project.models import Characters, Images
from project.helpers.db_session import db_session


def character_get(character: Characters):
    '''
    Render the character edit page.
    
    :param character: the character to be edited
    :return: The character page.
    '''
    edit_form = CharEdit(prefix="a")
    edit_form.bio.data = character.bio
    return render_template(
        "edit/character.html",
        editform=edit_form,
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
    with db_session(autocommit=False) as sess:
        if delform.submit.data:
            if delform.validate():
                flash(f"{character.name} deleted successfully.")
                character.removed = True
                sess.commit()
            else:
                return render_template(
                    "edit/character.html",
                    editform=editform,
                    character=character,
                    delform=delform,
                )
        elif editform.submit.data:
            if not editform.validate():
                return render_template(
                    "edit/character.html",
                    editform=editform,
                    character=character,
                    delform=delform,
                )
            if editform.img.data:
                character.img_id = Images.upload(editform.img.name)
            if editform.name.data:
                character.name = editform.name.data
            if editform.bio.data:
                character.bio = editform.bio.data
            sess.commit()
    return redirect(url_for("profile.characters"))
