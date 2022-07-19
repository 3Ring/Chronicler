from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms.validators import Length, Optional, DataRequired


class DMCreate(FlaskForm):
    name = StringField(
        '(Optional) Name different than default of "DM"',
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=50,
                message=f"name cannot be longer than %(max)d characters",
            ),
        ],
    )
    img = FileField(
        "(Optional) personalized DM Image",
        validators=[
            Optional(),
            FileAllowed(["jpg", "jpeg", "png"], "Images only!"),
            FileSize(500000, message="Image must be smaller than five megabytes"),
        ],
    )
    submit = SubmitField("Submit")
