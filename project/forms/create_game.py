from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms.validators import DataRequired, Length, Optional


class GameCreate(FlaskForm):
    name = StringField(
        "Name of your game",
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=50,
                message="Name cannot be longer than 50 characters",
            ),
        ],
    )
    img = FileField(
        "(Optional) Game Image",
        validators=[
            Optional(),
            FileAllowed(["jpg", "jpeg", "png"], "Images only!"),
            FileSize(5000000, message="Image must be smaller than five megabytes")
        ],
    )
    published = BooleanField("Publish? (Allow game to be searchable)")
    gamesubmit = SubmitField("Submit")
