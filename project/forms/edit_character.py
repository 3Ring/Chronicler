from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from project.forms.create_character import CharCreate


class CharEdit(CharCreate):
    pass


class CharDelete(FlaskForm):
    confirm = StringField(
        "Confirm by typing the name of the character you want to delete here"
    )
    char_del_submit = SubmitField("Delete")
