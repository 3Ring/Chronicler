from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from flask import flash, request

from project.models import Users as m_Users

def _failure(message=None):
    """redirect user back to /register on failure with flashed message"""
    if message:
        flash(message)
    return

def _success(message=None):
    """redirect user to /login on successful registration"""
    if message:
        flash(message)
    return


class User():
    """server side validation for user data"""

    @classmethod
    def register(cls, form):
        if not form:
            cls._failure("No data sent to server")
            return False
        error_name = cls.name(form.name.data)
        if type(error_name) is str:
            cls._failure(error_name)
            return False
        error_email = cls._register_email(form.email.data)
        if type(error_email) is str:
            cls._failure(error_email)
            return False
        
        error_password = cls.set_password(form.password.data, form.confirm.data)
        if type(error_password) is str:
            cls._failure(error_password)
            return False
        cls._success(f"Welcome to the table {form.name.data}!")
        return True

    @staticmethod
    def _failure(message=None):
        """redirect user back to /register on failure with flashed message"""
        if message:
            flash(message)
        return
    
    @staticmethod
    def _success(message=None):
        """redirect user to /login on successful registration"""
        if message:
            flash(message)
        return

    @classmethod
    def login(cls, form):
        message = 'Please check your login details and try again.'
        user = m_Users.query_by_email(form.email.data)
        if not user:
            cls._failure("not user")
            return False
        if not form:
            cls._failure("No data sent to server")
            return False
        error_email = cls.email(form.email.data)
        if type(error_email) is str:
            cls._failure(error_email)
            return False
        error_password = cls.check_password(form.password.data, user.hashed_password)
        if type(error_password) is str:
            cls._failure("password")
            return False
        return user

    @staticmethod
    def name(name):
        if not name:
            return "server didn't receive a name"
        elif type(name) is not str:
            return "name was not in text format"
        elif len(name) > 20:
            return "name cannot be over 20 characters"
        elif len(name) < 2:
            return "name must be at least 2 characters"
        return True

    @staticmethod
    def email(email):
        if not email:
            return "server didn't receive an email address"
        elif type(email) is not str:
            return "email address was not in text format"
        elif "@" not in email:
            return f"{email} is an invalid address"
        return True

    @classmethod 
    def _register_email(cls, email):
        error = cls.email(email)
        if type(error) is str:
            return error
        elif m_Users.query_by_email(email):
            return f"{email} is already in use!"
        return True

    @staticmethod
    def _password(password):
        if not password:
            return "server didn't receive a password"
        elif type(password) is not str:
            return "password was not in text format"
        elif len(password) < 8:
            return "password must be at least 8 characters"
        return True

    @classmethod
    def check_password(cls, password, hashed):
        password_error = cls._password(password)
        if type(password_error) is str:
            return password_error
        elif not check_password_hash(hashed, password):
            return "incorrect password"
        return True

    @classmethod
    def set_password(cls, password, confirm):
        password_error = cls._password(password)
        if type(password_error) is str:
            return password_error
        elif password != confirm:
            return "passwords do not match"
        return True
        
class Image():

    @classmethod
    def upload_and_parse(cls, filename: str) -> dict:
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
    def create(form):
        """validates game creation data and uploads img if exists
        
        returns are different based on outcome

        :param form: the WTForm used

        :return False: return if form wasn't able to be validated
        :return 'no image': return if no image was uploaded
        :return dict['pic']: the streamable filestorage of the image.
        :return dict['secure_name']: secure version of the filename
        :return dict['mimetype']: content type
        """
        if not form:
            _failure("No data sent to server")
            return False
        if not form.gamesubmit.data:
            _failure("No game data sent to server")
            return False
        img_data = Image.upload_and_parse(form.img.name)
        if not img_data:
            return "no image"
        elif type(img_data) is str:
            _failure(img_data)
            return False
        return img_data


class Character():

    @staticmethod
    def dm_create(form):
        """validates dm avatar creation data and uploads img if exists
        
        returns are different based on outcome

        :param form: the WTForm used

        :return False: return if form wasn't able to be validated
        :return 'no image': return if no image was uploaded
        :return dict['pic']: the streamable filestorage of the image.
        :return dict['secure_name']: secure version of the filename
        :return dict['mimetype']: content type
        """
        
        if not form:
            _failure("No data sent to server")
            return False
        if not form.dm_char_submit.data:
            _failure("No game data sent to server")
            return False
        img_data = Image.upload_and_parse(form.img.name)
        if not img_data:
            return "no image"
        elif type(img_data) is str:
            _failure(img_data)
            return False
        return img_data