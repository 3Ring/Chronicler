import os
from dotenv import load_dotenv

def _get_root(start_path: str, directory: str) -> str:
    root, tail = os.path.split(os.path.abspath(start_path))
    while tail != "":
        if tail == directory:
            return os.path.join(root, tail)
        root, tail = os.path.split(root)
    raise Exception(f"{directory} doesn't exist within given path: {start_path}")


def get_test_images_path(start_path: str) -> str:
    return os.path.join(start_path, "testing/test_images")

def load_env():
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".test_env"))
    load_dotenv(verbose=True, dotenv_path=dotenv_path)
    print(f'os.environ.get("ROOT_DIR_NAME"): {os.environ.get("ROOT_DIR_NAME")}')
    ROOT_DIR_PATH = _get_root(__file__, os.environ.get("ROOT_DIR_NAME"))
    os.environ.update({"ROOT_DIR_PATH": ROOT_DIR_PATH})
    os.environ.update(
        {"TEST_IMAGES_PATH": get_test_images_path(os.environ.get("ROOT_DIR_PATH"))}
    )

