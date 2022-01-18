from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, FileField
from wtforms.fields.simple import HiddenField
from wtforms.validators import Length, Optional


class GameEdit(FlaskForm):
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
    img = FileField("Game Image")
    published = BooleanField("Allow game to be searchable")
    edit_submit = SubmitField("Submit Changes")


class GameDelete(FlaskForm):
    name = StringField("Confirm here")
    game_delete_submit = SubmitField("Delete")


class GameManagePlayers(FlaskForm):
    players = SelectField("Players")
    player_id = HiddenField()
    player_submit = SubmitField("Remove Player")


class GameManageCharacters(FlaskForm):
    characters = SelectField("characters")
    character_id = HiddenField()
    character_submit = SubmitField("Remove Character")
