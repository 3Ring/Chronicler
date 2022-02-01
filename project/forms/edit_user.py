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
    user_edit_name_submit = SubmitField("Submit")


class UserEditEmail(FlaskForm):
    email = StringField("Change Email", validators=[DataRequired(), Email()])
    user_edit_email_submit = SubmitField("Submit")


class UserEditPassword(FlaskForm):
    password = PasswordField(
        "Change Password", validators=[DataRequired(), v.password_param]
    )
    confirm = PasswordField("Confirm New Password", validators=[DataRequired()])
    def validate_confirm(form, field):
        v.password_param(form, field)
        v.password_confirm(form, field)

    reveal = BooleanField("Show Passwords")
    user_edit_password_submit = SubmitField("Submit")


class UserDelete(FlaskForm):
    confirm = StringField("Confirm here", validators=[v.delete_account_confirm])
    user_delete_submit = SubmitField("Delete")
