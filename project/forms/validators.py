from string import ascii_letters, digits
from wtforms.validators import ValidationError
from werkzeug.security import check_password_hash
from flask_login import current_user

from project.models import BridgeGameCharacters, BridgeUserGames, Users


def email_user_exists(form, field):
    """
    If the user doesn't exist, raise a ValidationError

    :param form: The form that is currently being processed.
    :param field: The field to validate.
    """
    if not Users.query.filter_by(email=form.email.data).first():
        raise ValidationError(
            "There was a issue with your login. Check your credentials"
        )


def password_param(form, field):
    """
    Validate that the password is at least 8 characters long and no more than 100 characters

    :param form: The form that is currently being processed.
    :param field: The field to validate.
    """
    if type(field.data) is not str:
        raise ValidationError("data is invalid or corrupted")
    if len(field.data) < 8:
        raise ValidationError("Password must be at least 8 characters long")
    elif len(field.data) > 100:
        raise ValidationError("Password cannot be more than 100 characters")


def password_compare(form, field):
    """
    If the password in the form doesn't match the one in the database, raise a ValidationError

    :param form: The form that is currently being processed.
    :param field: The field to validate.
    """
    user = Users.query.filter_by(email=form.email.data).first()
    if not check_password_hash(user.hashed_password, field.data):
        raise ValidationError(
            "There was a issue with your login. Check your credentials"
        )


def password_confirm(form, field):
    """
    If the password and confirm password fields do not match, raise a ValidationError

    :param form: The form that is currently being processed.
    :param field: The field to validate.
    """
    if form.password.data != field.data:
        raise ValidationError("Passwords do not match")


def remove_player(form, field):
    """
    If the user is not in the game, raise a ValidationError

    :param form: The form that is currently being processed.
    :param field: The field to validate.
    """
    if not BridgeUserGames.query.filter_by(
        game_id=form.game_id.data, user_id=field.data
    ):
        raise ValidationError("Player not in game")


def remove_self_player(form, field):
    """
    If the user is not in the game, or the game name confimation does not match, raise a validation error

    :param form: The form that is currently being processed.
    :param field: The field to validate.
    """
    if not BridgeUserGames.query.filter_by(
        game_id=form.game_id.data, user_id=current_user.id
    ):
        raise ValidationError("Player not in game")
    if form.game_name.data.lower() != field.data.lower():
        raise ValidationError("Names do not match")


def add_character(form, field):
    """
    If the character is already in the game, raise a validation error

    :param form: The form that is currently being processed.
    :param field: The field to validate.
    """
    if BridgeGameCharacters.query.filter_by(
        character_id=field.data, game_id=form.game_id.data
    ).first():
        raise ValidationError("Character Already in Game")


def remove_character(form, field):
    """
    If the character is not in the game, raise a validation error

    :param form: The form that is currently being processed.
    :param field: The field to validate.
    """
    if not BridgeGameCharacters.query.filter_by(
        game_id=form.game_id.data, character_id=field.data
    ):
        raise ValidationError("Character not in game")


def delete_game_confirm(form, field):
    """
    If the game name confirmation doesn't match, raise a ValidationError

    :param form: The form that is currently being processed.
    :param field: The field to validate.
    """
    if form.game_name.data.lower() != field.data.lower():
        raise ValidationError("Game name does not match")


def delete_account_confirm(form, field):
    """
    If the email address confirmation doesn't match, raise a validation error

    :param form: The form that is currently being processed.
    :param field: The field to validate.
    """
    if form.email.data != field.data:
        raise ValidationError("Email does not match")


def delete_character_confirm(form, field):
    """
    If the character name confirmation doesn't match, raise a validation error

    :param form: The form that is currently being processed.
    :param field: The field to validate.
    """

    if form.char_name.data != field.data:
        raise ValidationError("Name does not match")

def is_ascii(form, field):
    if type(field.data) is not str:
        raise ValidationError(f"{field.name} only accepts ascii characters")
    for letter in field.data:
        if not letter.isalnum() and not letter.isspace():
            raise ValidationError(f'"{letter}" is not a valid input. {field.name} only accepts ascii characters')
