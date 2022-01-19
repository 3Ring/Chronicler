from wtforms.validators import ValidationError
from werkzeug.security import check_password_hash


from project.models import Users

def email_user_exists(form, field):
    if not Users.query.filter_by(email=form.email.data).first():
        raise ValidationError("There was a issue with your login. Check your credentials")

def password_param(form, field):
    if len(field.data) < 8:
        raise ValidationError("Password must be at least 8 characters long")
    elif len(field.data) > 100:
        raise ValidationError("Password cannot be more than 100 characters")

def password_compare(form, field):

    user = Users.query.filter_by(email=form.email.data).first()
    if not check_password_hash(user.hashed_password, field.data):
        raise ValidationError("There was a issue with your login. Check your credentials")

def password_confirm(form, field):
    if form.password.data != field.data:
        raise ValidationError("Passwords do not match")
