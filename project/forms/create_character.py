from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import Length, Optional


class CharCreate(FlaskForm):

    name = StringField(
        "Name",
        validators=[
            Optional(),
            Length(
                min=1,
                max=50,
                message=f"New name must be between %(min)d and %(max)d characters",
            ),
        ],
    )
    img = FileField("(Optional) Character Image")
    bio = TextAreaField("Bio")
    char_submit = SubmitField("Submit")
