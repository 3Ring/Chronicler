from itertools import count
from testing import Logger

LOGGER = Logger()
ITERATOR = count()

WINDOW_SIZE = (1920, 1080)
WINDOW_SIZES_LARGE = [(3840, 2160), (7680, 4320)]

URL_AUTH_REGISTER = "/register"
URL_AUTH_LOGIN = "/"
URL_AUTH_REAUTH = "/reauth"
URL_AUTH_LOGOUT = "/logout"
URL_INDEX = "/index"
URL_CREATE_GAME = "/create/game"
URL_CREATE_DM = "/create/dm"
URL_CREATE_CHARACTER = "/create/character"
URL_NOTES = "/notes"
URL_JOIN = "/join"
URL_PROFILE_CHARACTERS = "/profile/characters"
URL_PROFILE_ACCOUNT = "/profile/account"
URL_EDIT_ACCOUNT = "/edit/account"
URL_EDIT_ACCOUNT_DELETE = "/edit/account/delete"
URL_EDIT_CHARACTERS_PRE = "/edit/character/"

ADDOPT_HELP = {
    "--timeout": "same as `--timeout` except this used when you expect the test to fail",
    "--fail_timeout": "same as `--timeout` except this used when you expect the test to fail",
    "--poll_frequency": "used by `WebDriverWait` to set the poll_frequency on failure",
    "--browser_types": """used to set which browsers to run tests on. Tests will be rerun with every type. (Options: "chrome", "firefox", "edge", "all"(will run with every type))(default: "chome")""",
    "--log": """used to set the logging level. Choices are: (DEBUG, INFO, WARNING, ERROR, CRITICAL)""",
}

