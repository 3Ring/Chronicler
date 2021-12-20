
from project.models import *
from project.__init__ import db



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


def nuke():

    db.session.query(Notes).delete()
    print("Notes")
    db.session.commit()

    db.session.query(Sessions).delete()
    print("Sessions")
    db.session.commit()

    db.session.query(Items).delete()
    print("Loot")
    db.session.commit()

    db.session.query(Places).delete()
    print("Places")
    db.session.commit()

    db.session.query(NPCs).delete()
    print("NPCs")
    db.session.commit()

    db.session.query(Characters).delete()
    print("Characters")
    db.session.commit()

    db.session.query(BridgeUserGames).delete()
    print("Players")
    db.session.commit()

    db.session.query(Games).delete()
    print("Games")
    db.session.commit()

    db.session.query(Images).delete()
    print("Images")
    db.session.commit()

    db.session.query(Users).delete()
    print("Users")
    db.session.commit()

    return "database reset"


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

