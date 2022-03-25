import subprocess
from asyncio.subprocess import PIPE, STDOUT

from project.models import (
    Users,
    Images,
    Games,
    Characters,
    Sessions,
    Notes,
    Places,
    NPCs,
    Items,
    BridgeUserImages,
    BridgeUserGames,
    BridgeGameCharacters,
    BridgeGamePlaces,
    BridgeGameNPCs,
    BridgeGameItems,
)
from project.setup import defaults as d
from project.extensions.sql_alchemy import db
from project.helpers.db_session import db_session
from project.setup.db_init_create.base_items import Base_items

models = [
    Users,
    Images,
    Games,
    Characters,
    Sessions,
    Notes,
    Places,
    NPCs,
    Items,
    BridgeUserImages,
    BridgeUserGames,
    BridgeGameCharacters,
    BridgeGamePlaces,
    BridgeGameNPCs,
    BridgeGameItems,
]


def command(cmd: str) -> str:
    """
    Run a terminal command in a subprocess and return the output

    :param cmd: The command to run
    """
    return subprocess.run(
        cmd,
        stdout=PIPE,
        stderr=STDOUT,
        shell=True,
        cwd=(get_root(__file__)),
    )


def build(app):
    """
    This function initializes the database with the admin and orphanage rows

    :param app: The Flask app object
    """
    Base_items.init_database_assets(app)
    admins = [
        Users,
        Characters,
        Games,
    ]
    for a in admins:
        assert a.query.get(d.Admin.id) is not None
    for m in models:
        assert m.query.get(d.Orphanage.id) is not None


def _reset_empty():
    """
    Reset the database to an empty state
    """
    with db_session():
        for m in models:
            db.session.query(m).delete()
    for m in models:
        assert len(m.query.all()) == 0


def generate_user(fp, confirm_field=True):
    """
    Generate a user dictionary with the following unique keys: name, email, and password.

    :param fp: The file pointer to the file that stores the current value of the counter
    :return: A dictionary with the user's name, email, and password.
    """
    i = get_and_increment(fp) if type(fp) is not int else fp

    user = (
        {
            "name": f"User{i}",
            "email": f"User{i}@email.com",
            "password": f"User{i}password!@#$%^&*()-=./,'\"",
            "confirm": f"User{i}password!@#$%^&*()-=./,'\"",
        }
        if confirm_field
        else {
            "name": f"User{i}",
            "email": f"User{i}@email.com",
            "password": f"User{i}password!@#$%^&*()-=./,'\"",
        }
    )
    return user


def generate_game(fp):

    i = get_and_increment(fp) if type(fp) is not int else fp

    game = {
        "name": f"Game{i}",
        "publish": True,
    }

    return game


def alter_dict(item: dict, **kw):
    altered = item.copy()
    for k, v in kw.items():
        altered[k] = v
    return altered


def get_and_increment(fp):
    """
    used to create unique database items
    Read the file, increment the integer, and write the file

    :param fp: The file pointer to the file that stores the counter
    :return: the value of the counter.
    """
    fp.seek(0)
    it = int(fp.read())
    fp.seek(0)
    fp.write(str(it + 1))
    return it


def create_user(users):
    """
    Create a user in the database

    :param users: A list of dictionaries containing the user data
    """
    if type(users) is not list:
        users = [users]
    with db_session():
        [Users.create(**user) for user in users]
    for user in users:
        assert Users.query.filter_by(email=user["email"]).first() is not None


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


# def _nav_exists(driver):
#     """
#     check to make sure base navbar is loaded on page

#     :param driver: The WebDriver instance that we want to use to find the element
#     """
#     wait_for_element(driver, (By.TAG_NAME, "nav"))
#     wait_for_element(driver, (By.XPATH, "//a[@href='/index']"))
#     with pytest.raises(NoSuchElementException):
#         wait_for_element(driver, (By.XPATH, "//a[@href='/admin']"), timeout=1)


# def anon_nav(driver):
#     """
#     The function checks if the navigation bar exists on the page.
#     If it does, it waits for the "Home" and "Register" links to be visible.

#     :param driver: the webdriver object
#     """
#     _nav_exists(driver)
#     wait_for_element(driver, (By.XPATH, "//a[@href='/']"))
#     wait_for_element(driver, (By.XPATH, "//a[@href='/register']"))


# def auth_nav(driver):
#     """
#     check to make sure the navigation bar exists with links for logout, profile, and bugs


#     :param driver: the webdriver object
#     """
#     _nav_exists(driver)
#     wait_for_element(driver, (By.XPATH, "//a[@href='/logout']"))
#     wait_for_element(driver, (By.XPATH, "//a[@href='/profile']"))
#     wait_for_element(driver, (By.XPATH, "//a[@href='/bugs']"))


# def wait_for_url(driver, url: str, timeout: int = 10):
#     """
#     Wait for the URL to match the given URL

#     :param driver: The WebDriver instance that we want to wait for
#     :param url: The URL to wait for
#     :param timeout: The maximum number of seconds to wait for the expected condition to be true,
#     defaults to 10 (optional)
#     """
#     WebDriverWait(driver, timeout).until(expected_conditions.url_matches(url))
#     assert driver.current_url == url
def chron_url(url="/", **kw):
    import urllib.parse

    if kw:
        qstr = "?" + urllib.parse.urlencode(kw)
    else:
        qstr = ""
    return "http://localhost:5001" + url + qstr


# def input_element(driver, element, input_: str):

#     element.send_keys(input_)
#     updated = wait_for_element(driver, (By.ID, element.get_attribute("id")))
#     assert input_ == updated.get_attribute("value")
#     return updated


# def click_element(driver, locator):
#     """
#     Click the element that is located by the given locator

#     :param driver: The webdriver object
#     :param locator: The locator to wait for. This is in the format (By.<attr>, <locator string>)
#     """
#     el = wait_for_element(driver, locator)
#     el.click()
