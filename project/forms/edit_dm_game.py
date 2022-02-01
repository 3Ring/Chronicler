from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.simple import HiddenField
from wtforms.validators import (
    Length,
    Optional,
    DataRequired,
    InputRequired,
)

from project.forms import validators as v


class Edit(FlaskForm):
    name = StringField(
        "Change your game's name",
        validators=[
            Optional(),
            Length(
                min=1,
                max=50,
                message=f"New name must be between %(min)d and %(max)d characters",
            ),
        ],
    )
    img = FileField(
        "(Optional) Game Image",
        validators=[
            Optional(),
            FileAllowed(["jpg", "jpeg", "png"], "Images only!"),
        ],
    )
    published = BooleanField("Allow game to be searchable")
    edit_submit = SubmitField("Submit Changes")


class Delete(FlaskForm):
    confirm = StringField(
        "Confirm deletion by entering game name here",
        validators=[DataRequired(), v.delete_game_confirm],
    )
    game_delete_submit = SubmitField("Delete")
    # used for form validation
    game_name = HiddenField()


class RemovePlayer(FlaskForm):
    players = SelectField(
        "Players",
        coerce=int,
        validators=[DataRequired(), InputRequired(), v.remove_player],
    )
    submit = SubmitField("Remove Player")
    # used for form validation
    game_id = HiddenField()

    def __init__(self, game_id=None, choices=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if choices:
            self.players.choices = [(g.id, g.name) for g in choices]
        if game_id:
            self.game_id.data = game_id


class RemoveCharacter(FlaskForm):
    characters = SelectField(
        "characters",
        coerce=int,
        validators=[DataRequired(), InputRequired(), v.remove_character],
    )
    submit = SubmitField("Remove Character")
    # used for form validation
    game_id = HiddenField()

    def __init__(self, game_id=None, choices=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if choices:
            self.characters.choices = [(g.id, g.name) for g in choices]
        if game_id:
            self.game_id.data = game_id
