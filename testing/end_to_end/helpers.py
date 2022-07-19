import os
import json
import urllib.parse


def bool_convert(val):
    return val if type(val) is not str else json.loads(val)


def query_string_convert(**kw):
    return "?" + urllib.parse.urlencode(kw)


def url_convert(url: str = None) -> str:
    if url is None:
        url = os.environ.get("DEFAULT_URL")
    return os.environ.get("ROOT_URL") + url


def redirect(intended_url: str, redirect_url: str) -> str:
    return redirect_url + query_string_convert(next=intended_url)


def bad_images_path():
    path = os.path.abspath(os.path.join(os.environ.get("TEST_IMAGES_PATH"), "fail"))
    _, _, files = next(os.walk(path))
    return [os.path.abspath(os.path.join(path, file)) for file in files]


# def make_game(
#     user: dict,
#     name: str = None,
#     publish: bool = True,
# ):
#     game = {"dm_id": user["id"]}
#     game["name"] = f"NAME_{user['name']}" if name is None else name
#     game["publish"] = publish
#     game["players"] = []
#     return game

# def make_character(
#     user_name: str, 
# )
# def make_dm(user_name: str, dm_name: str = None):
#     return f"DM_{user_name}" if dm_name is None else dm_name
