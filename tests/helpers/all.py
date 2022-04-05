from io import TextIOWrapper
from asyncio import SelectorEventLoop
import asyncio

# async def make_id(fp: TextIOWrapper, loop: SelectorEventLoop) -> int:
#     future = asyncio.run_coroutine_threadsafe(
#         asyncio.to_thread(get_and_increment, fp), loop
#     )
#     return await asyncio.wrap_future(future, loop=loop)
def make_id(fp: TextIOWrapper) -> int:
    return get_and_increment(fp)

def generate_user(_id, confirm_field: bool = True) -> dict:
    """
    Generate a user dictionary with the following unique keys: name, email, and password.

    :param fp: The file pointer to the file that stores the current value of the counter
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

    game = {
        "name": f"Game{_id}",
        "publish": publish,
    }

    return game


def alter_dict(item: dict, **kw) -> dict:
    altered = item.copy()
    for k, v in kw.items():
        altered[k] = v
    return altered


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


def get_root(file):
    """
    Get the root directory of the Chronicler package

    :param file: The file to be loaded
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
    import urllib.parse

    if kw:
        qstr = "?" + urllib.parse.urlencode(kw)
    else:
        qstr = ""
    return "http://localhost:5001" + url + qstr
