from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import Length, Optional


class CharCreate(FlaskForm):

    name = StringField(
        "Name",
        validators=[
            Length(
                min=1,
                max=50,
                message=f"New name must be between %(min)d and %(max)d characters",
            ),
        ],
    )
    img = FileField(
        "(Optional) Character Image",
        validators=[
            Optional(),
            FileAllowed(["jpg", "jpeg", "png"], "Images only!"),
        ],
    )
    bio = TextAreaField(
        "Bio",
        validators=[
            Optional(),
            Length(
                min=1,
                max=5000,
                message=f"Bio must be between %(min)d and %(max)d characters",
            ),
        ],
    )
    submit = SubmitField("Submit")
