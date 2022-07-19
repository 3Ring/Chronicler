from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email
from wtforms.validators import ValidationError

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

    def validate_email(form, field):
        from project.models import Users

        if Users.query.filter_by(email=field.data).first():
            raise ValidationError("This email is already registered with an account")
        DataRequired(),
        Length(
            min=6,
            max=120,
            message=f"Game name must be between %(min)d and %(max)d characters",
        ),
        # TODO this needs to be changed when implimenting email support
        if len(field.data) > 0 and not field.data[0].isalnum():
            raise ValidationError("Invalid email")
        Email(),

    email = StringField("Email")
    password = PasswordField("Password", validators=[DataRequired(), v.password_param])
    confirm = PasswordField("Confirm Password", validators=[DataRequired()])

    def validate_confirm(form, field):
        v.password_param(form, field)
        v.password_confirm(form, field)

    reveal = BooleanField("Show Passwords")
    usersubmit = SubmitField("Submit")
