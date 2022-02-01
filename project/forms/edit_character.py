from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField

from project.forms.create_character import CharCreate
from project.forms import validators as v


class CharEdit(CharCreate):
    pass


class CharDelete(FlaskForm):
    char_name = HiddenField()
    confirm = StringField(
        "Confirm by typing the name of the character you want to delete here",
        validators=[v.delete_character_confirm],
    )
    submit = SubmitField("Delete")

    def __init__(self, char_name=None, *args, **kw):
        super().__init__(*args, **kw)
        if char_name:
            self.char_name.data = char_name
