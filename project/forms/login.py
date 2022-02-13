from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired

from project.forms import validators as v


class Login(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def validate_password(form, field):
        # the email is checked here as well so that the error will only print under the password field regardless of which field threw the error
        v.email_user_exists(form, field)
        v.password_compare(form, field)

    remember = BooleanField("Remember Me")
    submit = SubmitField("Submit")
