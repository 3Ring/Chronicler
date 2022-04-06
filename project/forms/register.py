from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email

from project.forms import validators as v


class Register(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=20,
                message=f"Game name must be between %(min)d and %(max)d characters",
            ),
            v.is_ascii,
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Length(
                min=6,
                max=120,
                message=f"Game name must be between %(min)d and %(max)d characters",
            ),
            Email(),
        ],
    )
    password = PasswordField("Password", validators=[DataRequired(), v.password_param])
    confirm = PasswordField("Confirm Password", validators=[DataRequired()])

    def validate_confirm(form, field):
        v.password_param(form, field)
        v.password_confirm(form, field)

    reveal = BooleanField("Show Passwords")
    usersubmit = SubmitField("Submit")
