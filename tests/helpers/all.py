import urllib.parse
from io import TextIOWrapper


def make_id(fp: TextIOWrapper) -> int:
    """
    It reads the current value of the counter from the file and increments it.
    this is superfluous and should be removed
    
    :return: The id of the question.
    """
    return get_and_increment(fp)


def generate_user(_id, confirm_field: bool = True) -> dict:
    """
    Generate a dictionary of user data.
    
    :param _id: The unique id of the user
    :param confirm_field: If True, the confirm field will be present in the user data, defaults to True

    :return: A dictionary with the user's name, email, and password.
    """

    user = (
        {
            "name": f"User{_id}",
            "email": f"User{_id}@email.com",
            "password": f"User{_id}password!@#$%^&*()-=./,'\"",
            "confirm": f"User{_id}password!@#$%^&*()-=./,'\"",
        }
        if confirm_field
        else {
            "name": f"User{_id}",
            "email": f"User{_id}@email.com",
            "password": f"User{_id}password!@#$%^&*()-=./,'\"",
        }
    )
    return user


def generate_game(_id, publish: bool = True) -> dict:
    """
    Generate a game object

    :param _id: The id of the game
    :param publish: If True, the game will be published on server. If False, the game will be private,
    defaults to True
    :return: A dictionary with the name of the game and whether or not it is published.
    """

    game = {
        "name": f"Game{_id}",
        "publish": publish,
    }

    return game


def get_and_increment(fp: TextIOWrapper) -> int:
    """
    used to create unique database items
    Read the file, increment the integer, and write the file

    :param fp: The file pointer to the file that stores the counter
    :return: the value of the counter.
    """
    fp.seek(0)
    re = fp.read()
    it = int(re)
    fp.seek(0)
    fp.write(str(it + 1))
    return it


def get_root(file: str):
    """
    Get the root directory of the Chronicler package

    :param file: The chronicler subdirectory
    :return: The root directory of the chronicler repository.
    """
    import os

    root = file
    head, tail = os.path.split(root)
    while tail != "":
        root = head
        head, tail = os.path.split(head)
        if tail == "chronicler":
            return root
    raise BaseException("directory doesn't exist")


def chron_url(url="/", **kw):
    """
    appends the given subdirectory to the chronicler test server root.

    :param **kw: takes the kw as a dict and parses it as a query_string to be appended to the url
    :param url: The Chronicler subdirectory , defaults to / (optional)
    :return: A string.
    """

    if kw:
        qstr = "?" + urllib.parse.urlencode(kw)
    else:
        qstr = ""
    return "http://localhost:5001" + url + qstr
