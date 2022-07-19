import os


def set_heroku():
    """this is to set the address for Flask socket.io"""
    heroku = False
    if os.environ.get("HEROKU_HOSTING"):
        heroku = True
    return heroku

def bool_convert(priv):
    if type(priv) is bool:
        return priv
    if type(priv) is str and priv.lower() == "true":
        return True
    return False
