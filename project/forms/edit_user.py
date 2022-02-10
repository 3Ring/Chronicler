from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email
from project.forms import validators as v


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
    submit = SubmitField("Submit")


class UserEditEmail(FlaskForm):
    email = StringField("Change Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")


class UserEditPassword(FlaskForm):
    password = PasswordField(
        "Change Password", validators=[DataRequired(), v.password_param]
    )
    confirm = PasswordField("Confirm New Password", validators=[DataRequired()])
    def validate_confirm(form, field):
        v.password_param(form, field)
        v.password_confirm(form, field)

    reveal = BooleanField("Show Passwords")
    submit = SubmitField("Submit")


class UserDelete(FlaskForm):
    confirm = StringField("Confirm here", validators=[v.delete_account_confirm])
    submit = SubmitField("Delete")
