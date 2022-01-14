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
from wtforms.fields.simple import HiddenField
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


class UserEditName(FlaskForm):
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
    user_edit_name_submit = SubmitField("Submit")

class UserEditEmail(FlaskForm):
    email = StringField("Change Email", validators=[DataRequired()])
    user_edit_email_submit = SubmitField("Submit")

class UserEditPassword(FlaskForm):
    password = PasswordField("Change Password", validators=[DataRequired(), password])
    confirm = PasswordField("Confirm New Password", validators=[DataRequired()])
    reveal = BooleanField("Show Passwords")
    user_edit_password_submit = SubmitField("Submit")


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
    published = BooleanField("Allow game to be searchable")
    edit_submit = SubmitField("Submit Changes")


class GameTransfer(FlaskForm):

    heir = SelectField("Players")
    transfer_player = StringField("Player's name")
    transfer_game = StringField("Game's name")
    transfer_init = SubmitField("Transfer Ownership")
    transfer_transfer = SubmitField("Transfer")
    transfer_confirm = SubmitField("Confirm")


class GameManagePlayers(FlaskForm):
    players = SelectField("Players")
    player_id = HiddenField()
    player_submit = SubmitField("Remove Player")


class GameManageCharacters(FlaskForm):
    characters = SelectField("characters")
    character_id = HiddenField()
    character_submit = SubmitField("Remove Character")


class GameEnd(FlaskForm):
    end_init = SubmitField("End Game")
    end_confirm = SubmitField("End Game")


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
