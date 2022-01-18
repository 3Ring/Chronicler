from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField

from wtforms.validators import Length, Optional


class DMCreate(FlaskForm):
    name = StringField(
        '(Optional) Name different than default of "DM"',
        validators=[
            Optional(),
            Length(
                min=1,
                max=50,
                message=f"New name must be between %(min)d and %(max)d characters",
            ),
        ],
    )
    img = FileField("(Optional) personalized dm Image")
    dm_char_submit = SubmitField("Submit")
