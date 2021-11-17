from datetime import datetime
import base64

from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import orm
from flask import request

from .__init__ import db

imageLink__defaultGame = "/static/images/default_game.jpg"
decoder = "data:;base64,"


class SABaseMixin(object):

    @classmethod
    def query_from_id(cls, id_):
        return cls.query.filter_by(id = id_).first()

    @classmethod
    def create(cls, **kw):
        """adds new User to db"""
        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit()
        return obj

    def __repr__(self) -> str:
        repr_ = f"{self.__tablename__}("
        print("sup")
        for column in self.__table__.columns:
            repr_ += f"{column.key}={getattr(self, str(column.key))}, "
        repr_ = repr_[:-2] + ")"

        return repr_

class Users(SABaseMixin, db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    hashed_password = db.Column(db.String(120), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    characters = db.relationship('Characters', backref='user', lazy=True)

    self_title = "user"

    @staticmethod
    def get_admin():
        """Returns admin User object"""
        
        return Users.query.filter_by(email="app@chronicler.gg").first()
        
    @classmethod
    def create(cls, **kw):
        """adds new User to db"""
        kw["hashed_password"] = generate_password_hash(kw["password"], method='sha256')
        kw.pop("password")
        super().create(**kw)

class Games(SABaseMixin , db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    secret = db.Column(db.Integer, default=0)
    published = db.Column(db.Boolean, default=False, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    dm_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    img_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    image = imageLink__defaultGame
    self_title = "game"
    places = db.relationship('Places', backref='game', lazy=True)
    NPCs = db.relationship('NPCs', backref='game', lazy=True)

    players = db.relationship('Users', secondary='players', lazy='subquery',
        backref=db.backref('games', lazy=True))

    @orm.reconstructor
    def init_on_load(self):
        self.image_object = Images.query_from_id(self.img_id)
        if self.image_object is not None:
            self.image = Images.add_decoder(self.image_object)


    @staticmethod
    def get_index_lists(User) -> dict:
        """Returns a dictionaty containing the game lists that the player is in.

        Where dict['player_list'] is a list of Game objects the User is listed as a player in, 
        and dict['dm_list'] is a list of Game objects the User is listed in as the 'DM'. """
        game_lists = {}
        
        
        game_lists["player_list"]=Games.query.filter(
            Games.dm_id != User.id,
            Games.id.in_(
            Players.query.with_entities(Players.games_id).
            filter(Players.users_id.in_(
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
        super().create(**kw)
        # add tutorial notes and session zero to game
        cls.new_game_training_wheels()

    def new_game_training_wheels(self):
        """add tutorial notes and session zero to game"""
        
        tutorial_user=Users.get_admin()
        # add tutorial character
        tutorial_character = Characters.create(name="Chronicler Helper", user_id=tutorial_user.id, game_id=self.id)
        Sessions.create(number=0, title="The Adventure Begins!", games_id=self.id)


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

class Players(SABaseMixin, db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    games_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)

    self_title = "player"

class Sessions(SABaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    synopsis = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    games_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)

    @classmethod
    def get_list_from_gameID(cls, game_id) -> list:
        """returns list of sessions in order of Sessions.number"""

        session_list=Sessions.query.filter_by(games_id=game_id).order_by(Sessions.number).all()
        return session_list

class Notes(SABaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # make not nullable
    charname=db.Column(db.String(50))
    note = db.Column(db.Text)
    session_number = db.Column(db.Integer)
    private = db.Column(db.Boolean)
    to_gm = db.Column(db.Boolean)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    char_img = "/static/images/default_character.jpg"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    character = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)

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
            self.char_img = Images.add_decoder(self.image_object.img)
        elif self.charname == "DM":
            self.char_img = "/static/images/default_dm.jpg"



def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
    for i, letter in enumerate(filename):
        if letter == '/':
            altered = (filename[i+1:]).lower()
            break
    
    if altered in ALLOWED_EXTENSIONS:
        return True
    return False

def render_picture(data):

    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic

class Images(SABaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # should be changed to "img_string"
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    self_title = "image"

    @staticmethod
    def add_decoder(image_object):
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
        if not allowed_file(mimetype):
            return "Not allowed file type. Image must be of type: .png .jpg or .jpeg"

        secure = secure_filename(pic.filename)
        
        if not secure or not mimetype:
            return 'Bad upload!'

        pic.stream.seek(0)
        data = pic.stream.read()
        render_file = render_picture(data)

        img = Images.create(img=render_file, name=secure, mimetype=mimetype)
        _id = img.id

        return _id 

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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    img_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    image = "/static/images/default_character.jpg"
    
    self_title = "character"

    @orm.reconstructor
    def init_on_load(self):
        if self.img_id == None:
            self.image_object = None
        else:
            self.image_object = Images.query_from_id(self.img_id)
            self.image = Images.add_decoder(self.image_object.img)


class NPCs(SABaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    secret_name = db.Column(db.String(40))
    bio = db.Column(db.Text, default='A Mysterious Individual')
    secret_bio = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    self_title = "NPC"

class Places(SABaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    bio = db.Column(db.Text, default='A Place of Mystery')
    secret_bio = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    NPCs = db.relationship('NPCs', backref='place', lazy=True)
    self_title = "place"

class Loot(SABaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    bio = db.Column(db.Text, default='An item shrouded in mystery')
    copper_value = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    self_title = "loot"


