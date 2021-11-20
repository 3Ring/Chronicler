from datetime import datetime
import base64

from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import orm, text
from flask import request

from .__init__ import db

imageLink__defaultGame = "/static/images/default_game.jpg"
decoder = "data:;base64,"


#######################################
###           Base classes         ####
#######################################

class SABaseMixin(object):

    id = db.Column(db.Integer, primary_key=True)
    removed = db.Column(db.Boolean, default=False, server_default=text("FALSE"))

    @classmethod
    def query_from_id(cls, id_: int):
        return cls.query.filter_by(id = id_).first()

    @classmethod
    def create(cls, **kw):
        """adds new User to database"""
        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit()
        return obj

    def remove_self(self):
        self.removed=True

    def _delete_attached(self, dependencies: list = [], confirm: bool = False):
        """deletes all attached items
        
        :param dependencies: list containing lists of dependencies
        :param confirm: confirmation to make sure this wasn't 
                        used on accident when "remove_self" method was intended
        """
        if confirm:
            for list in dependencies:
                self._delete_list(list, confirm=confirm)
        return 

    def _delete_list(self, item_list: list, confirm: bool = False):
        """deletes all items in argument list
        
        :param item_list: list of SQLAlchemy objects to delete
        :param confirm: confirmation to make sure this wasn't 
                        used on accident when "remove_self" method was intended
        """
        if confirm:
            for item in item_list:
                item.delete_self(confirm=confirm)
        return

    def delete_self(self, confirm: bool = False):
        """deletes SQLAlchemy model from database.

        :param confirm: confirmation to make sure this wasn't 
                        used on accident when "remove_self" method was intended
        """
        if confirm:
            self._delete_attached(confirm=confirm)
            db.session.query(self.__class__).filter_by(id=self.id).delete()
            db.session.commit()

    def __repr__(self) -> str:
        repr_ = f"{self.__tablename__}("
        print("sup")
        for column in self.__table__.columns:
            repr_ += f"{column.key}={getattr(self, str(column.key))}, "
        repr_ = repr_[:-2] + ")"

        return repr_


#######################################
###           Main tables          ####
#######################################

class Users(SABaseMixin, db.Model, UserMixin):
    
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    hashed_password = db.Column(db.String(120), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    self_title = "user"

    @staticmethod
    def get_admin():
        """Returns admin User object"""
        
        return Users.query.filter_by(email="app@chronicler.gg").first()
        
    @staticmethod
    def add_to_bug_report_page(email):
        """Creates a User character and adds them to the bug report page
        it's done this way because the bug report page uses the "notes" page's code so it requires a "Character".
        """

        user = Users.query_by_email(email)
        Characters.create(name=user.name, user_id=user.id, game_id=-1)
        return

    @classmethod
    def query_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def create(cls, **kw):
        """adds new User to database and hashes their password.
        it also adds the user to bug reports
        """
        kw["hashed_password"] = generate_password_hash(kw["password"], method='sha256')
        kw.pop("password")
        user = super().create(**kw)
        cls.add_to_bug_report_page(kw["email"])
        return user

    def orphan_attached(self):
        """changes the dm ID to the admin"""

        admin = Users.get_admin()
        games_list = Games.query.filter_by(dm_id=self.id).all()
        for game in games_list:
            game.dm_id = admin.id

    def delete_attached(self, confirm: bool = False):
        """deletes all attached items
        
        :param confirm: confirmation to make sure this wasn't 
                        used on accident when "remove_self" method was intended
        """
        if confirm:
            dependencies = []
            dependencies.append(Games.query.filter_by(dm_id=self.id).all())
            dependencies.append(Characters.query.filter_by(user_id=self.id).all())
            dependencies.append(Notes.query.filter_by(origin_user_id=self.id).all())
            dependencies.append(Players.query.filter_by(user_id=self.id).all())
            dependencies.append(Images.query.filter_by(user_id=self.id).all())
            for list in dependencies:
                self._delete_list(list, confirm=confirm)

    def delete_self(self, confirm: bool = False, orphan: bool = True):
        """deletes user from database.

        :param confirm: confirmation to make sure this wasn't 
                        used on accident when "remove_self" method was intended
        :param orphan: if set to `True` will set dependencies to be owned by admin
                       if `False` dependencies will be deleted 
        """
        if confirm:
            if orphan:
                self.orphan_attached(confirm=confirm)
            else:
                self.delete_attached(confirm=confirm)
            return super().delete_self(confirm=confirm)
        return

class Games(SABaseMixin , db.Model):

    name = db.Column(db.String(50), nullable=False)
    secret = db.Column(db.Integer, default=0, server_default=text("0"))
    published = db.Column(db.Boolean, default=False, server_default=text("FALSE"), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    dm_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    img_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    image = imageLink__defaultGame
    self_title = "game"
    # places = db.relationship('Places', backref='game', lazy=True)
    # NPCs = db.relationship('NPCs', backref='game', lazy=True)

    # players = db.relationship('Users', secondary='players', lazy='subquery',
    #     backref=db.backref('games', lazy=True))

    @orm.reconstructor
    def init_on_load(self):
        self.image_object = Images.query_from_id(self.img_id)
        if self.image_object is not None:
            self.image = Images._add_decoder(self.image_object)


    @staticmethod
    def get_index_lists(User) -> dict:
        """Returns a dictionary containing the game lists that the player is in.

        Where dict['player_list'] is a list of Game objects the User is listed as a player in, 
        and dict['dm_list'] is a list of Game objects the User is listed in as the 'DM'. """
        game_lists = {}
        
        
        game_lists["player_list"]=Games.query.filter(
            Games.dm_id != User.id,
            Games.id.in_(
            Players.query.with_entities(Players.game_id).
            filter(Players.user_id.in_(
            Users.query.with_entities(
            Users.id).filter_by(
            id=User.id))))
        ).all()
        game_lists["dm_list"]=Games.query.filter_by(dm_id=User.id).all()

        for game in game_lists["player_list"]:
            img = Images.query.filter_by(id=game.img_id).first()
            if not img:
                game.image = imageLink__defaultGame
            else:
                game.image = decoder + img.img
        for game in game_lists["dm_list"]:
            img = Images.query.filter_by(id=game.img_id).first()
            if not img:
                game.image = imageLink__defaultGame
            else:
                game.image = decoder + img.img
        return game_lists

    @classmethod
    def create(cls, **kw):
        """adds new Game to db"""
        obj = super().create(**kw)
        # add tutorial notes and session zero to game
        cls.new_game_training_wheels(obj)
        return obj

    def _delete_attached(self, confirm: bool = False):
        """deletes all attached items
        
        :param confirm: confirmation to make sure this wasn't 
                        used on accident when "remove_self" method was intended
        """
        if confirm:
            dependencies = []
            dependencies.append(Notes.query.filter_by(game_id=self.id).all())
            dependencies.append(Sessions.query.filter_by(game_id=self.id).all())
            dependencies.append(Players.query.filter_by(game_id=self.id).all())
            dependencies.append(BridgeCharacters.query.filter_by(game_id=self.id).all())
            dependencies.append(BridgeNPCs.query.filter_by(game_id=self.id).all())
            dependencies.append(BridgePlaces.query.filter_by(game_id=self.id).all())
            dependencies.append(BridgeItems.query.filter_by(game_id=self.id).all())

            return super()._delete_attached(dependencies, confirm=confirm)


    def new_game_training_wheels(self):
        """add tutorial notes and session zero to game"""
        
        tutorial_user=Users.get_admin()
        # add tutorial character
        tutorial_character = Characters.create(name="Chronicler Helper", user_id=tutorial_user.id, game_id=self.id)
        Sessions.create(number=0, title="The Adventure Begins!", game_id=self.id)


        tutorial_notes = []
        note_texts = [
            # note 1
            '''
            <p><strong class="ql-size-huge"><u>Intro Note 1:</u></strong></p><p>Welcome to your next great adventure!</p><p><br></p><p>This is a place where you can write and share notes.</p>
            ''',
            # note 2
            '''
            <p><strong class="ql-size-huge"><u>Intro Note 2:</u></strong></p><p>Notes are ordered by "Session" by which we typically mean game session, but for you it can mean whatever you want!</p><p><br></p><p>For your "Session Zero" notes I recommend you have notes related to the overall shape of your game. A short list would be:</p><p><br></p><ol><li>house rules</li><li>areas of roleplay and story that are off limits due to player comfort</li><li>expectations</li></ol><ul><li>how long each session should be</li><li>how often you plan to meet</li><li>what you will do if a player can't make it</li><li>etc!</li></ul>
            ''',
            # note 3
            '''
            <p><strong class="ql-size-huge"><u>Intro Note 3:</u></strong></p><p>you can edit and delete your notes whenever you like, and though you can't typically delete other player's note, you are more than welcome to get rid of mine if you are already experts!</p>
            ''',
            # note 4
            '''
            <p><strong class="ql-size-huge"><u>Intro note 4:</u></strong></p><p>Right now this site is in an Alpha phase, which means Chronicler is just a baby!</p><p><br></p><p>If you notice anything that seems broken or could be improved please let me know so I can make it better!</p>
            ''',
            # note 5
            '''
            <p><strong class="ql-size-huge"><u>Intro Note 5:</u></strong></p><p>This is the last note in the session!</p><p><br></p><p><em>Then why is it at the top?</em></p><p><br></p><p>Chronicler is designed to be a collaborative note taking application. That means that it's meant to be used while you are playing together! We think it's better if the newest notes appear at the top of the page.</p><p><br></p><p>Don't worry, you can change this if you like....<strong>(eventually)</strong></p>
            '''
        ]

        for note in note_texts:
            tutorial_notes.append(Notes.create(charname="Chronicler Helper", note=note, session_number=0, user_id=tutorial_user.id, character=tutorial_character.id, game_id=self.id))

class Sessions(SABaseMixin, db.Model):

    number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    synopsis = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)

    @classmethod
    def get_list_from_gameID(cls, game_id) -> list:
        """returns list of sessions in order of Sessions.number"""

        session_list=Sessions.query.filter_by(game_id=game_id).order_by(Sessions.number).all()
        return session_list

class Notes(SABaseMixin, db.Model):

    # make not nullable
    charname=db.Column(db.String(50))
    note = db.Column(db.Text)
    session_number = db.Column(db.Integer)
    private = db.Column(db.Boolean)
    to_gm = db.Column(db.Boolean)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    char_img = "/static/images/default_character.jpg"

    origin_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    origin_character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)

    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    self_title = "note"
    header = "note."

    @classmethod
    def get_list_from_session_number(cls, session_number, game_id):
        return cls.query.filter_by(game_id=game_id).filter_by(session_number=session_number).order_by(Notes.date_added).all()

    @orm.reconstructor
    def init_on_load(self):
        character_object = Characters.query.filter_by(name=self.charname, game_id=self.game_id).first()
        self.image_object = Images.query_from_id(character_object.img_id)
        if self.image_object is not None:
            self.char_img = Images._add_decoder(self.image_object.img)
        elif self.charname == "DM":
            self.char_img = "/static/images/default_dm.jpg"

class Images(SABaseMixin, db.Model):

    # should be changed to "img_string"
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    self_title = "image"
    # need to fix this with config file and add all past images to users
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), default=1, server_default=text("1"), nullable=False)

    @staticmethod
    def _allowed_file(filename):
        ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
        for i, letter in enumerate(filename):
            if letter == '/':
                altered = (filename[i+1:]).lower()
                break
        
        if altered in ALLOWED_EXTENSIONS:
            return True
        return False

    @staticmethod
    def _render_picture(data):

        render_pic = base64.b64encode(data).decode('ascii') 
        return render_pic

    @staticmethod
    def _add_decoder(image_object):
        """adds decoder prefix for base 64 image strings"""
        decoder2 = f"data:{image_object.mimetype};base64,"
        return decoder2 + image_object.img

    @staticmethod
    def upload(filename):
        try:
            pic = request.files[filename]
        except:
            return 'Invalid file or filename'

        if not pic:
            return -1

        if len(pic.stream.read()) > 3000000:
            return 'image is too large. limit to images 1MB or less.'

        mimetype = pic.mimetype
        if not Images._allowed_file(mimetype):
            return "Not allowed file type. Image must be of type: .png .jpg or .jpeg"

        secure = secure_filename(pic.filename)
        
        if not secure or not mimetype:
            return 'Bad upload!'

        pic.stream.seek(0)
        data = pic.stream.read()
        render_file = Images._render_picture(data)

        img = Images.create(img=render_file, name=secure, mimetype=mimetype)
        id_ = img.id

        return id_ 

    @staticmethod
    def make_character_images(character_id):
        character = Characters.query_from_id(character_id)
        image = Images.query_from_id(character.id)
        # set defaults if no image exists
        
        if image == None:
            if character.name == "DM":
                return "/static/images/default_dm.jpg"
            else:
                return "/static/images/default_character.jpg"
        else:
            decoder2 = f"data:{image.mimetype};base64, "
            return decoder2 + image.img

class Characters(SABaseMixin, db.Model):

    name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    img_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    image = "/static/images/default_character.jpg"
    
    self_title = "character"

    @classmethod
    def create(cls, **kw):
        """Creates a new character and adds player to relational table"""
        character = super().create(**kw)
        Players.create(user_id=kw["user_id"], game_id=kw["game_id"])
        return character

    def _delete_attached(self, confirm: bool = False):
        """deletes all attached items
        
        :param confirm: confirmation to make sure this wasn't 
                        used on accident when "remove_self" method was intended
        """
        if confirm:
            dependencies = []
            dependencies.append(Notes.query.filter_by(origin_character_id=self.id).all())
            dependencies.append(BridgeCharacters.query.filter_by(character_id=self.id).all())
            return super()._delete_attached(dependencies, confirm=confirm)

    @orm.reconstructor
    def init_on_load(self):
        if self.img_id == None:
            self.image_object = None
        else:
            self.image_object = Images.query_from_id(self.img_id)
            self.image = Images._add_decoder(self.image_object.img)

class NPCs(SABaseMixin, db.Model):
    __tablename__ = "npcs"

    name = db.Column(db.String(40), nullable=False)
    secret_name = db.Column(db.String(40))
    bio = db.Column(db.Text, default='A Mysterious Individual')
    secret_bio = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    

    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    self_title = "NPC"

    def _delete_attached(self, confirm: bool = False):
        """deletes all attached items
        
        :param confirm: confirmation to make sure this wasn't 
                        used on accident when "remove_self" method was intended
        """
        if confirm:
            dependencies = []
            dependencies.append(BridgeNPCs.query.filter_by(npc_id=self.id).all())
            return super()._delete_attached(dependencies, confirm=confirm)
class Places(SABaseMixin, db.Model):

    name = db.Column(db.String(40), nullable=False)
    bio = db.Column(db.Text, default='A Place of Mystery')
    secret_bio = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    self_title = "place"

    def _delete_attached(self, confirm: bool = False):
        """deletes all attached items
        
        :param confirm: confirmation to make sure this wasn't 
                        used on accident when "remove_self" method was intended
        """
        if confirm:
            dependencies = []
            dependencies.append(BridgePlaces.query.filter_by(place_id=self.id).all())
            return super()._delete_attached(dependencies, confirm=confirm)

class Items(SABaseMixin, db.Model):

    name = db.Column(db.String(40), nullable=False)
    bio = db.Column(db.Text, default='An item shrouded in mystery')
    copper_value = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    self_title = "loot"

    def _delete_attached(self, confirm: bool = False):
        """deletes all attached items
        
        :param confirm: confirmation to make sure this wasn't 
                        used on accident when "remove_self" method was intended
        """
        if confirm:
            dependencies = []
            dependencies.append(BridgeItems.query.filter_by(item_id=self.id).all())
            return super()._delete_attached(dependencies, confirm=confirm)


#######################################
###       Many-to-many tables      ####
#######################################

class Players(SABaseMixin, db.Model):
    """multi-relational database joining Users and Games"""
    __tablename__ = 'players'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)

    self_title = "player"

class BridgeCharacters(SABaseMixin, db.Model):
    """multi-relational database joining character game assets"""
    __tablename__ = "bridgecharacters"

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))

class BridgeNPCs(SABaseMixin, db.Model):
    """multi-relational database joining NPC game assets"""
    __tablename__ = "bridgenpcs"

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    npc_id = db.Column(db.Integer, db.ForeignKey("npcs.id"))

class BridgePlaces(SABaseMixin, db.Model):
    """multi-relational database joining Place game assets"""
    __tablename__ = "bridgeplaces"

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"))

class BridgeItems(SABaseMixin, db.Model):
    """multi-relational database joining character item assets"""
    __tablename__ = "bridgeitems"

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
