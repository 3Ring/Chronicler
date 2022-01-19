from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Optional


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
    img = FileField(
        "(Optional) Game Image",
        validators=[
            Optional(),
            FileAllowed(["jpg", "jpeg", "png"], "Images only!"),
        ],
    )
    published = BooleanField("Publish? (Allow game to be searchable)")
    gamesubmit = SubmitField("Submit")
