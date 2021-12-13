import os
from datetime import datetime


#######################################
###            Base                ####
#######################################
# Values are set to none so they won't cause errors in the creation methods
class Base:
    removed = False
    server_removed = "FALSE"
    date_added = datetime.utcnow()
    admin_email = os.environ.get("ADMIN_EMAIL")
    orphin_email = os.environ.get("ORPHAN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASS")


class Images:
    orphanage = "/static/images/orphanage.jpg"
    user_admin = "/static/images/_user_admin.jpg"
    user_list = [
        "/static/images/ChromnIcon2.png",
        "/static/images/ChromnIcon3.png",
        "/static/images/ChromnIcon4.png",
        "/static/images/ChromnIcon5.png",
        "/static/images/ChromnIcon6.png",
        "/static/images/ChromnIcon7.png",
    ]
    game = "/static/images/default_game.jpg"
    game_bugs = "/static/images/_bugs.jpg"
    games_dm = "/static/images/dm_games.jpeg"
    games_player = "/static/images/player_games.jpg"
    character_player = "/static/images/default_character.jpg"
    character_dm = "/static/images/default_dm.jpg"


class Orphanage:
    id = int(os.environ.get("ORPHANAGE_ID"))
    image = Images.orphanage


class Admin:
    id = int(os.environ.get("ADMIN_ID"))


#######################################
###            Users               ####
#######################################


class User(Base):
    image = Images.user_list[0]


class UserAdmin(Admin, User):
    password = Base.admin_password
    name = "Admin User"
    email = Base.admin_email
    image = Images.user_admin


class UserOrphanage(Orphanage, User):
    name = "Orphan User"
    password = Base.admin_password
    email = Base.orphin_email
    image = Images.orphanage


#######################################
###            Games              ####
#######################################


class Game(Base):
    published = False
    server_published = "FALSE"
    image = Images.game
    image_object = None
    dm_id = Orphanage.id
    img_id = None


class GameBugs(Admin, Game):
    name = "Bug Reports and Comments"
    dm_id = Admin.id
    image = Images.game_bugs


class GameOrphanage(Orphanage, Game):
    name = "Orphan Game"


#######################################
###           Character            ####
#######################################


class Character(Base):
    bio = None
    copy = False
    dm = False
    avatar = False
    img_id = None
    img_object = object
    server_dm = "FALSE"
    server_avatar = "FALSE"
    server_copy = "FALSE"
    image = Images.character_player


class CharacterTutorial(Admin, Character):
    name = "Chronicler Helper"
    bio = "A very happy helper"
    avatar = True
    user_id = Admin.id


class CharacterOrphanage(Orphanage, Character):
    name = "Orphan Character"
    user_id = Orphanage.id


#######################################
###           Session              ####
#######################################


class Session(Base):
    synopsis = None


class SessionOrphanage(Orphanage, Session):
    number = 0
    title = "orphanage"
    game_id = Orphanage.id


#######################################
###           Notes                ####
#######################################


class Note(Base):
    char_img = Images.character_player


class NoteOrphanage(Orphanage, Note):
    charname = "Orphanage"
    text = "Orphanage text"
    session_number = 0
    private = False
    to_dm = False

    def _get_char_img(self):
        return Orphanage.image

    char_img = property(_get_char_img)

    user_id = Orphanage.id
    origin_character_id = Orphanage.id

    game_id = Orphanage.id


#######################################
###           Images               ####
#######################################


class Image(Base):
    pass


class ImageOrphanage(Orphanage, Image):
    img_string = "Orphanage"
    name = "Orphanage"
    mimetype = "Orphanage"


#######################################
###           NPCs                 ####
#######################################
class NPC(Base):
    bio = "A Mysterious Individual"


class NPCOrphanage(Orphanage, NPC):
    name = "Orphanage"
    secret_name = None
    bio = "Orphanage"
    secret_bio = None
    img_id = Orphanage.id
    place_id = Orphanage.id
    user_id = Orphanage.id


#######################################
###           Places               ####
#######################################


class Place(Base):
    bio = "A Place of Mystery"


class PlaceOrphanage(Orphanage, Place):
    name = "Orphanage"
    bio = None
    secret_bio = None


#######################################
###            Items               ####
#######################################


class Item(Base):
    bio = "An item shrouded in mystery"


class ItemOrphanage(Orphanage, Base):
    name = "Orphanage"
    bio = "An item shrouded in mystery"
    copper_value = None


#######################################
###            Bridges             ####
#######################################


class BridgeUserImage(Base):
    pass


class BridgeUserImageOrphanage(Orphanage, BridgeUserImage):
    user_id = Orphanage.id
    img_id = Orphanage.id


class BridgeUserGame(Base):
    owner = False
    server_owner = "FALSE"


class BridgeUserGameOrphanage(Orphanage, BridgeUserGame):
    owner = True
    user_id = Orphanage.id
    game_id = Orphanage.id


class BridgeCharacter(Base):
    dm = False
    server_dm = "FALSE"


class BridgeGameCharacterOrphanage(Orphanage, BridgeCharacter):
    dm = True
    character_id = Orphanage.id
    game_id = Orphanage.id


class BridgePlace(Base):
    pass


class BridgeGamePlaceOrphanage(Orphanage, BridgePlace):
    place_id = Orphanage.id
    game_id = Orphanage.id


class BridgeGameNPC(Base):
    pass


class BridgeGameNPCOrphanage(Orphanage, BridgeGameNPC):
    npc_id = Orphanage.id
    game_id = Orphanage.id


class BridgeItem(Base):
    pass


class BridgeGameItemOrphanage(Orphanage, BridgeItem):
    item_id = Orphanage.id
    game_id = Orphanage.id
