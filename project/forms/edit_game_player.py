from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired


class CharAdd(FlaskForm):
    character = SelectField("Your Characters", validators=[InputRequired()])
    char_add_submit = SubmitField("Add to Game")


class CharRemove(FlaskForm):
    character = SelectField("Your Characters", validators=[InputRequired()])
    char_remove_submit = SubmitField("Remove from game")


class LeaveGame(FlaskForm):
    confirm = StringField("Confirm here")
    leave_submit = SubmitField("Leave")
