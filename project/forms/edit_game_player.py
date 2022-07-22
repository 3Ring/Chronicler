from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectMultipleField
from wtforms.validators import InputRequired, DataRequired
from project.forms import validators as v
from wtforms import widgets


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CharAdd(FlaskForm):

    character = MultiCheckboxField(
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

