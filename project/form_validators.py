from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from flask import flash, request


def _failure(message, super_message=None):
    if super_message:
        message=super_message
    if message:
        flash(message)
    return False

def _success(message, super_message=None):
    if super_message:
        message=super_message
    if message:
        flash(message)
    return True

def _missing_form(form):
    if not form:
        return True

def _is_email(email):
    if not email:
        return "server didn't receive an email address"
    elif type(email) is not str:
        return "email address was not in text format"
    elif "@" not in email or "." not in email:
        return f"{email} is an invalid address"
    return True

def _matching_password(password, confirm):
    password_error = _password(password)
    if type(password_error) is str:
        return password_error
    elif password != confirm:
        return "passwords do not match"
    return True


def _password(password):
    if not password:
        return "server didn't receive a password"
    elif type(password) is not str:
        return "password was not in text format"
    elif len(password) < 8:
        return "password must be at least 8 characters"
    return True
class User():
    """server side validation for user data"""

    @staticmethod
    def remove(form, user, failure_message=None, success_message=None):
        print(form.confirm.data.lower().strip(), user.email.lower().strip())
        if not _is_email(form.confirm.data):
            return _failure("server didn't understand data", failure_message)
        elif form.confirm.data.lower().strip() != user.email.lower().strip():
            return _failure("names do not match", failure_message)
        return _success(success_message)

    @classmethod
    def register(cls, form, failure_message=None, success_message=None):
        if _missing_form(form):
            return _failure(failure_message)
        error_name = cls._name(form.name.data)
        if type(error_name) is str:
            return _failure(error_name, failure_message)
        error_email = _is_email(form.email.data)
        if type(error_email) is str:
            return _failure(error_email, failure_message)
        error_password = _matching_password(form.password.data, form.confirm.data)
        if type(error_password) is str:
            return _failure(error_password, failure_message)
        return _success(f"Welcome to the table {form.name.data}!", success_message)

    @classmethod
    def edit(cls, form, failure_message=None, success_message=None):
        if _missing_form(form):
            return False
        if form.name.data:
            error_name = cls._name(form.name.data)
            if type(error_name) is str:
                return _failure(error_name, failure_message)
        if form.email.data:
            error_email = _is_email(form.email.data)
            if type(error_email) is str:
                return _failure(error_email, failure_message)
        if form.password.data:
            error_password = _matching_password(form.password.data, form.confirm.data)
            if type(error_password) is str:
                return _failure(error_password, failure_message)
        return _success("Changes saved", success_message)

    @classmethod
    def user(cls, form, failure_message=None, success_message=None):
        if _missing_form(form):
            return _failure(failure_message)
        error_email = _is_email(form.email.data)
        if type(error_email) is str:
            return _failure(failure_message)
        return _success(success_message)


    @staticmethod
    def _name(name):
        if not name:
            return "server didn't receive a name"
        elif type(name) is not str:
            return "name was not in text format"
        elif len(name) > 20:
            return "name cannot be over 20 characters"
        elif len(name) < 2:
            return "name must be at least 2 characters"
        return True

    @classmethod
    def check_password(cls, password, hashed, failure_message=None, success_message=None):
        password_error = _password(password)
        if type(password_error) is str:
            return _failure(password_error, failure_message)
        elif not check_password_hash(hashed, password):
            return _failure("incorrect password", failure_message)
        return _success(success_message)


        
class Image():

    @classmethod
    def _upload_and_parse(cls, filename: str) -> dict:
        """checks and parses image upload data
        
        :param filename: file name string ex 'img' 
                        this correlates to the 'name' value in the file form input field.
        
        :return dict['pic']: the streamable filestorage of the image.
        :return dict['secure_name']: secure version of the filename
        :return dict['mimetype']: content type
        """
        try:
            pic = request.files[filename]
        except:
            return 'Invalid image file or filename. Images must be in .jpg or .png format'
        if not pic:
            return False
        if len(pic.stream.read()) > 3000000:
            return 'image is too large. limit to images 1MB or less.'
        
        mimetype = pic.mimetype
        if not mimetype:
            return 'Invalid image file or filename. Images must be in .jpg or .png format'
        allowed = cls._allowed_file(mimetype)
        if type(allowed) is str:
            return allowed
        secure_name = secure_filename(pic.filename)
        if not secure_name:
            return "Bad Upload!"
        return {"pic": pic
                , "secure_name": secure_name
                , "mimetype": mimetype
                }

    @staticmethod
    def _allowed_file(filename):
        ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
        for i, letter in enumerate(filename):
            if letter == '/':
                altered = (filename[i+1:]).lower()
                break
        if altered in ALLOWED_EXTENSIONS:
            return True
        return "Not allowed file type. Image must be of type: .png .jpg or .jpeg"

class Game():

    @staticmethod
    def create(form, failure_message=None, success_message=None):
        """validates game creation data and uploads img if exists
        
        returns are different based on outcome

        :param form: the WTForm used

        :return False: return if form wasn't able to be validated
        :return 'no image': return if no image was uploaded
        :return dict['pic']: the streamable filestorage of the image.
        :return dict['secure_name']: secure version of the filename
        :return dict['mimetype']: content type
        """
        if _missing_form(form):
            return _failure(failure_message)
        if not form.gamesubmit.data:
            return _failure(failure_message)
        img_data = Image._upload_and_parse(form.img.name)
        if not img_data:
            return "no image"
        elif type(img_data) is str:
            return _failure(img_data)
        return img_data


class Character():

    @staticmethod
    def remove(form, character, failure_message=None, success_message=None):
        print(form.confirm.data.lower().strip(), character.name.lower().strip())
        if type(form.confirm.data) != str:
            return _failure("server didn't understand data", failure_message)
        elif form.confirm.data.lower().strip() != character.name.lower().strip():
            return _failure("names do not match", failure_message)
        return _success(success_message)


    @staticmethod
    def create(form, failure_message=None, success_message=None):
        """validates dm avatar creation data and uploads img if exists
        
        returns are different based on outcome

        :param form: the WTForm used

        :return False: return if form wasn't able to be validated
        :return 'no image': return if no image was uploaded
        :return dict['pic']: the streamable filestorage of the image.
        :return dict['secure_name']: secure version of the filename
        :return dict['mimetype']: content type
        """

        if _missing_form(form):
            return _failure(failure_message)
        if not form.char_submit.data:
            return _failure(failure_message)
        img_data = Image._upload_and_parse(form.img.name)
        if not img_data:
            return "no image"
        elif type(img_data) is str:
            return _failure(img_data)
        _success(success_message)
        return img_data

    @staticmethod
    def dm_create(form, failure_message=None, success_message=None):
        """validates dm avatar creation data and uploads img if exists
        
        returns are different based on outcome

        :param form: the WTForm used

        :return False: return if form wasn't able to be validated
        :return 'no image': return if no image was uploaded
        :return dict['pic']: the streamable filestorage of the image.
        :return dict['secure_name']: secure version of the filename
        :return dict['mimetype']: content type
        """
        if _missing_form(form):
            return _failure(failure_message)
        if not form.dm_char_submit.data:
            return _failure(failure_message)
        img_data = Image._upload_and_parse(form.img.name)
        if not img_data:
            return "no image"
        elif type(img_data) is str:
            return _failure(img_data)
        return img_data
