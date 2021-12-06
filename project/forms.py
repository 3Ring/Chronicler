from re import S

# from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    BooleanField,
    SelectField,
    TextAreaField,
    IntegerField,
    FileField,
)
from wtforms.fields import core
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    Optional,
    ValidationError,
)

# from project import form_validators

from markupsafe import Markup
from wtforms.widgets.core import html_params


def password(form, field, message=None):
    if message is None:
        message = f"Password must be at least 8 characters long"
    if len(field.data) < 8:
        raise ValidationError(message)


# def image(form, field, filename):
#     message = form_validators.Image.upload_and_parse(filename)
#     if len(field.data) < 8:
#         raise ValidationError(message)
# Form models
class UserCreate(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=20,
                message=f"Game name must be between %(min)d and %(max)d characters",
            ),
        ],
    )
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), password])
    confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    reveal = BooleanField("Show Passwords")
    usersubmit = SubmitField("Submit")


class UserEdit(FlaskForm):
    name = StringField(
        "Change Name",
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=20,
                message=f"Game name must be between %(min)d and %(max)d characters",
            ),
        ],
    )
    email = StringField("Change Email", validators=[DataRequired()])
    password = PasswordField("Change Password", validators=[DataRequired(), password])
    confirm = PasswordField("Confirm New Password", validators=[DataRequired()])
    reveal = BooleanField("Show Passwords")
    user_edit_submit = SubmitField("Submit")


class Login(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=20,
                message=f"Game name must be between %(min)d and %(max)d characters",
            ),
        ],
    )
    password = PasswordField("Password", validators=[DataRequired(), password])
    email = StringField("Email", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Submit")


class UserDelete(FlaskForm):
    confirm = StringField("Confirm here")
    user_delete_submit = SubmitField("Delete")


class GameCreate(FlaskForm):
    name = StringField(
        "Name of your game",
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=50,
                message=f"Game name must be between %(min)d and %(max)d characters",
            ),
        ],
    )
    img = FileField("(Optional) Game Image")
    published = BooleanField("Publish? (Allow game to be searchable)")
    gamesubmit = SubmitField("Submit")


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
    private = BooleanField("Unpublish? (Do not allow game to be searchable)")
    published = BooleanField("Publish? (Allow game to be searchable)")
    game_edit_submit = SubmitField("Submit")


class GameRemove(FlaskForm):
    will = BooleanField("Transfer Game ownership to another specific user?")
    heir = SelectField("Users")
    name = StringField("Confirm here")
    game_remove_submit = SubmitField("Remove")


class GameDelete(FlaskForm):
    name = StringField("Confirm here")
    game_delete_submit = SubmitField("Delete")


class CharCreate(FlaskForm):

    name = StringField(
        "Name",
        validators=[
            Optional(),
            Length(
                min=1,
                max=50,
                message=f"New name must be between %(min)d and %(max)d characters",
            ),
        ],
    )
    img = FileField("(Optional) Character Image")
    bio = TextAreaField("Bio")
    char_submit = SubmitField("Submit")


class CharAdd(FlaskForm):
    character = SelectField("Your Characters", validators=[InputRequired()])
    char_add_submit = SubmitField("Add to Game")


class CharRemove(FlaskForm):
    character = SelectField("Your Characters", validators=[InputRequired()])
    char_remove_submit = SubmitField("Remove from game")


class CharDelete(FlaskForm):
    confirm = StringField(
        "Confirm by typing the name of the character you want to delete here"
    )
    char_del_submit = SubmitField("Delete")


class DMCreate(FlaskForm):
    name = StringField(
        '(Optional) Name different than default of "DM"',
        validators=[
            Optional(),
            Length(
                min=1,
                max=50,
                message=f"New name must be between %(min)d and %(max)d characters",
            ),
        ],
    )
    img = FileField("(Optional) personalized dm Image")
    dm_char_submit = SubmitField("Submit")


class DMNote(FlaskForm):
    characters = SelectField("Characters")


class LeaveGame(FlaskForm):
    confirm = StringField("Confirm here")
    leave_submit = SubmitField("Leave")
