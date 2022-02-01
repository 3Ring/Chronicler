from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import InputRequired, ValidationError, DataRequired
from project.models import BridgeGameCharacters
from project.forms import validators as v


class CharAdd(FlaskForm):

    character = SelectField(
        "Your Characters", coerce=int, validators=[DataRequired(), v.add_character]
    )
    # used for form validation
    game_id = HiddenField()
    submit = SubmitField("Add to Game")

    def __init__(self, game_id=None, choices=None, *args, **kw):
        super().__init__(*args, **kw)
        if choices:
            self.character.choices = [(g.id, g.name) for g in choices]
        if game_id:
            self.game_id.data = game_id


class LeaveGame(FlaskForm):
    confirm = StringField("Confirm here", validators=[InputRequired(), v.remove_self_player])
    # used for form validation
    game_id = HiddenField()
    game_name = HiddenField()
    submit = SubmitField("Leave")

    def __init__(self, game_id=None, game_name=None, *args, **kw):
        super().__init__(*args, **kw)
        if game_id:
            self.game_id.data = game_id
        if game_name:
            self.game_name.data = game_name

