import os
from project.models import *
from project.__init__ import db

def set_heroku():
    """this is to set the address for Flask socket.io"""
    heroku = False
    if os.environ.get("HEROKU_HOSTING"):
        heroku = True
    return heroku

def attach_game_image_or_default_from_Images_model(model):
    keys = ["img", "mimetype"]
    corrects = 0
    for key in keys:
        if key in model.__dict__.keys():
            corrects += 1
    if corrects == len(keys):
        image = f"data:{model.mimetype};base64,{model.img}"
    else:
        image = "/static/images/default_game.jpg"
    return image


def private_convert(priv):
    if type(priv) == bool:
        return priv
    elif type(priv) == str:
        if priv.lower() == "true":
            return True
        else:
            return False
    else:
        return False

