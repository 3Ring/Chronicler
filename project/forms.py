from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, TextAreaField, IntegerField, FileField
from wtforms.validators import DataRequired

# Form models
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired ()])
    confirm = PasswordField("Confirm Password", validators=[DataRequired ()])
    realname = StringField("Real Name (Optional)")
    reveal = BooleanField("Show Passwords")
    usersubmit = SubmitField("Submit")

class LoginForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired ()])
    email = StringField("Email", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Submit")

class CreateGameForm(FlaskForm):
    name = StringField("Name of your game")
    img = FileField("(Optional) Game Image")
    published = BooleanField("Publish? (Allow game to be searchable)")
    gamesubmit = SubmitField("Submit")

class CharForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    img = FileField("(Optional) Character Image")
    bio = TextAreaField("Bio")
    charsubmit = SubmitField("Submit")
