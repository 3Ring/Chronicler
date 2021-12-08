from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from flask import flash, request


def _failure(message, super_message=None):
    if super_message:
        message = super_message
    if message:
        flash(message)
    return False


def _success(message, super_message=None):
    if super_message:
        message = super_message
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


class User:
    """server side validation for user data"""

    @staticmethod
    def remove(form, user, failure_message=None, success_message=None):

        if not _is_email(form.confirm.data):
            return _failure("server didn't understand data", failure_message)
        elif form.confirm.data.lower().strip() != user.email.lower().strip():
            return _failure("names do not match", failure_message)
        return _success(success_message)

    @classmethod
    def register(cls, form, failure_message=None, success_message=None):
        if _missing_form(form):
            return _failure("no data received", failure_message)
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
    def check_password(
        cls, password, hashed, failure_message=None, success_message=None
    ):
        password_error = _password(password)
        if type(password_error) is str:
            return _failure(password_error, failure_message)
        elif not check_password_hash(hashed, password):
            return _failure("incorrect password", failure_message)
        return _success(success_message)


class Image:
    @classmethod
    def _valid(cls, filename):
        pic = request.files[filename]
        if len(pic.stream.read()) > 3000000:
            return "image is too large. limit to images 1MB or less."
        if not pic.mimetype:
            return (
                "Invalid image file or filename. Images must be in .jpg or .png format"
            )
        if not cls._allowed_file(pic.mimetype):
            return "Not allowed file type. Image must be of type: .png .jpg or .jpeg"
        if not secure_filename(pic.filename):
            return _failure("Bad Upload!")
        return True

    # @classmethod
    # def _upload_and_parse(cls, filename: str) -> dict:
    #     """checks and parses image upload data

    #     :param filename: file name string ex 'img'
    #                     this correlates to the 'name' value in the file form input field.

    #     :return dict['pic']: the streamable filestorage of the image.
    #     :return dict['secure_name']: secure version of the filename
    #     :return dict['mimetype']: content type
    #     """
    #     try:
    #         pic = request.files[filename]
    #     except:
    #         return 'Invalid image file or filename. Images must be in .jpg or .png format'
    #     if not pic:
    #         return False
    #     if len(pic.stream.read()) > 3000000:
    #         return 'image is too large. limit to images 1MB or less.'

    #     mimetype = pic.mimetype
    #     if not mimetype:
    #         return 'Invalid image file or filename. Images must be in .jpg or .png format'
    #     allowed = cls._allowed_file(mimetype)
    #     if type(allowed) is str:
    #         return allowed
    #     secure_name = secure_filename(pic.filename)
    #     if not secure_name:
    #         return "Bad Upload!"
    #     return {"pic": pic
    #             , "secure_name": secure_name
    #             , "mimetype": mimetype
    #             }

    @staticmethod
    def _allowed_file(filename):
        ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]
        for i, letter in enumerate(filename):
            if letter == "/":
                altered = (filename[i + 1 :]).lower()
                break
        if altered in ALLOWED_EXTENSIONS:
            return True
        return "Not allowed file type. Image must be of type: .png .jpg or .jpeg"


class Game:
    @classmethod
    def create(cls, form, failure_message=None, success_message=None):
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
        if form.img.data:
            return cls.image(form.img.name, failure_message, success_message)
        else:
            return _success(success_message)

    @staticmethod
    def edit(form, failure_message=None, success_message=None):

        if _missing_form(form):
            return _failure(failure_message)
        if not form.game_edit_submit.data:
            return _failure(failure_message)
        return _success(success_message)

    @staticmethod
    def name(name, failure_message=None, success_message=None):
        if not name:
            return _failure("server didn't receive a name", failure_message)
        elif type(name) is not str:
            return _failure("name was not in text format", failure_message)
        elif len(name) > 50:
            return _failure("name cannot be over 20 characters", failure_message)
        elif len(name) < 2:
            return _failure("name must be at least two characters", failure_message)
        return _success(success_message)

    @staticmethod
    def image(filename, failure_message=None, success_message=None):
        if not filename:
            return _failure("server didn't receive an image", failure_message)
        img_data = Image._valid(filename)
        if type(img_data) is str:
            return _failure(img_data, failure_message)
        return _success(success_message)

    @staticmethod
    def leave(form, failure_message=None, success_message=None):
        if _missing_form(form):
            return _failure("server didn't receive any data", failure_message)
        if type(form.confirm.data) is not str:
            return _failure("confirmation data corrupted", failure_message)
        return _success(success_message)

class Character:
    @staticmethod
    def remove(form, character, failure_message=None, success_message=None):
        if type(form.confirm.data) != str:
            return _failure("server didn't understand data", failure_message)
        elif form.confirm.data.lower().strip() != character.name.lower().strip():
            return _failure("names do not match", failure_message)
        return _success(success_message)

    @classmethod
    def add(cls, form, failure_message=None, success_message=None):
        """validates character add data

        :param form: the WTForm used
        :return False: return if form wasn't able to be validated
        :return True: return if form was able to be validated
        """

        if _missing_form(form):
            return _failure("server didn't receive any form data", failure_message)
        error_id = cls._id(form.character.data)
        if type(error_id) is str:
            return _failure(error_id, failure_message)
        return _success(success_message)

    @staticmethod
    def create(form, failure_message=None, success_message=None):
        """validates character creation data

        :param form: the WTForm used
        :return False: return if form wasn't able to be validated
        :return True: return if form was able to be validated
        """
        if _missing_form(form):
            return _failure(failure_message)
        if not form.char_submit.data:
            return _failure(failure_message)
        if form.img.data:
            return Game.image(form.img.name, failure_message, success_message)
        else:
            return _success(success_message)

    @staticmethod
    def dm_create(form, failure_message=None, success_message=None):
        """validates dm avatar creation data

        :param form: the WTForm used
        :return False: return if form wasn't able to be validated
        :return True: return if form was able to be validated
        """
        if _missing_form(form):
            return _failure(failure_message)
        if not form.dm_char_submit.data:
            return _failure(failure_message)
        if form.img.data:
            return Game.image(form.img.name, failure_message, success_message)
        else:
            return _success(success_message)

    @staticmethod
    def _id(id_):
        if not id_:
            return "Server didn't receive any data"
        if type(id_) is not int:
            try:
                _ = int(id_)
            except:
                return "id needs to be of type: int"
        return True

    @staticmethod
    def _name(name):
        if not name:
            return "Server didn't receive any name data"
        if type(name) is not str:
            return "name was not in text format"
        if len(name) > 50:
            return "Character name must be under 50 characters in length"
        if len(name) < 1:
            return "Character name must be at least 1 character in length"
        return True
