import os
from dotenv import load_dotenv

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

ADDOPT_HELP = {
    "--timeout": "same as `--timeout` except this used when you expect the test to fail",
    "--fail_timeout": "same as `--timeout` except this used when you expect the test to fail",
    "--poll_frequency": "used by `WebDriverWait` to set the poll_frequency on failure",
    "--browser_types": """used to set which browsers to run tests on. Tests will be rerun with every type. (Options: "chrome", "firefox", "edge", "all"(will run with every type))(default: "chome")""",
    "--log": """used to set the logging level. Choices are: (DEBUG, INFO, WARNING, ERROR, CRITICAL)""",
}

def _get_root(start_path: str, directory: str) -> str:
    root, tail = os.path.split(os.path.abspath(start_path))
    while tail != "":
        if tail == directory:
            return os.path.join(root, tail)
        root, tail = os.path.split(root)
    raise Exception(f"{directory} doesn't exist within given path: {start_path}")


def get_test_images_path(start_path: str) -> str:
    return os.path.join(start_path, "testing/test_images")

def _load_env():
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".test_env"))
    load_dotenv(verbose=True, dotenv_path=dotenv_path)
    print(f'os.environ.get("ROOT_DIR_NAME"): {os.environ.get("ROOT_DIR_NAME")}')
    ROOT_DIR_PATH = _get_root(__file__, os.environ.get("ROOT_DIR_NAME"))
    os.environ.update({"ROOT_DIR_PATH": ROOT_DIR_PATH})
    os.environ.update(
        {"TEST_IMAGES_PATH": get_test_images_path(os.environ.get("ROOT_DIR_PATH"))}
    )