from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length


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
