
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, TextAreaField, IntegerField, FileField
from wtforms.validators import DataRequired
from flask_login import UserMixin
from .__init__ import db


class Players(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    games_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)

    self_title = "player"
    def __repr__(self):
        return '< Player: %r >' % self



# Create Models for db
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    hash = db.Column(db.String(120), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    characters = db.relationship('Characters', backref='user', lazy=True)

    self_title = "user"
    def __repr__(self):
        return '< User.id: %r >' % self.id


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    secret = db.Column(db.Integer, default=0)
    published = db.Column(db.Boolean, default=False, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    dm_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    img_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    image = str
    self_title = "game"
    places = db.relationship('Places', backref='game', lazy=True)
    NPCs = db.relationship('NPCs', backref='game', lazy=True)


    players = db.relationship('Users', secondary='players', lazy='subquery',
        backref=db.backref('games', lazy=True))

    def __repr__(self):
        return '<Game %r>' % self.name

class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    synopsis = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    games_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    self_title = "session"
    header = "session."


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    charname=db.Column(db.String(50))
    note = db.Column(db.Text)
    session_number = db.Column(db.Integer)
    private = db.Column(db.Boolean)
    to_gm = db.Column(db.Boolean)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    character = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)

    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    self_title = "note"
    header = "note."

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    self_title = "image"

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    img_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    self_title = "character"
    # @classmethod
    # def create(cls, **kw):
    #     obj = cls(**kw)
    #     db.session.add(obj)
    #     db.session.commit()
    #     return obj
    # image = Images.query.with_entities(Images.img).filer_by(id = img_id).first()
    # print(image)


    def __repr__(self):
        return '<Character %r>' % self.name

class NPCs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    secret_name = db.Column(db.String(40))
    bio = db.Column(db.Text, default='A Mysterious Individual')
    secret_bio = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    self_title = "NPC"
    def __repr__(self):
        return '<NPC %r>' % self.name

class Places(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    bio = db.Column(db.Text, default='A Place of Mystery')
    secret_bio = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    NPCs = db.relationship('NPCs', backref='place', lazy=True)
    self_title = "place"
    def __repr__(self):
        return '<Place %r>' % self.name

class Loot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    bio = db.Column(db.Text, default='An item shrouded in mystery')
    copper_value = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    self_title = "loot"
    def __repr__(self):
        return '<Loot %r>' % self.name






# Form models
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    hash = PasswordField("Password", validators=[DataRequired ()])
    confirm = PasswordField("Confirm Password", validators=[DataRequired ()])
    realname = StringField("Real Name (Optional)")
    reveal = BooleanField("Show Passwords")
    usersubmit = SubmitField("Submit")

class LoginForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired ()])
    email = StringField("Email", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Submit")

class DeleteForm(FlaskForm):
    user_group_id = SelectField(u'Users', coerce=int)
    game_group_id = SelectField(u'Games', coerce=int)
    character_group_id = SelectField(u'Characters', coerce=int)
    npc_group_id = SelectField(u'NPCs', coerce=int)
    place_group_id = SelectField(u'Places', coerce=int)
    loot_group_id = SelectField(u'Loot', coerce=int)
    note_group_id = SelectField(u'Notes', coerce=int)
    session_group_id = SelectField(u'Notes', coerce=int)
    player_group_id = SelectField(u'Notes', coerce=int)
    submit = SubmitField("Submit")

class ConForm(FlaskForm):
    todelete = StringField("Item to Delete:")
    confirm = SubmitField("Confirm")
    cancel = SubmitField("Cancel")

class GameForm(FlaskForm):
    name = StringField("Name")
    img = FileField("(Optional) Game Image")
    sessions = IntegerField("Number of Sessions")
    secret = IntegerField("User who this game is attached to '0' if published")
    published = BooleanField("Publish? (Allow game to be searchable)")
    dm_id = IntegerField("User_id who this game is attached to")
    gamesubmit = SubmitField("Submit")

class CreateGameForm(FlaskForm):
    name = StringField("Name of your game")
    img = FileField("(Optional) Game Image")
    published = BooleanField("Publish? (Allow game to be searchable)")
    gamesubmit = SubmitField("Submit")

class NPCForm(FlaskForm):
    name = StringField("Name")
    secret_name = StringField("Secret Name")
    bio = TextAreaField("Bio")
    secret_bio = TextAreaField("Secret Bio")
    game_id = IntegerField("GameID")
    place_id = IntegerField("PlaceID")
    npcsubmit = SubmitField("Submit")

class CharForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    img = FileField("(Optional) Character Image")
    bio = TextAreaField("Bio")
    platinum = IntegerField("Platinum Pieces")
    gold = IntegerField("Gold Pieces")
    electrum = IntegerField("Electrum Pieces")
    silver = IntegerField("Silver Pieces")
    copper = IntegerField("Copper Pieces")
    experience = IntegerField("experience")
    strength = IntegerField("Strength")
    dexterity = IntegerField("Dexterity")
    constitution = IntegerField("Constitution")
    wisdom = IntegerField("Wisdom")
    intelligence = IntegerField("Intelligence")
    charisma = IntegerField("Charisma")
    user_id = IntegerField("UserID")
    game_id = IntegerField("GameID")
    charsubmit = SubmitField("Submit")

class PlaceForm(FlaskForm):
    name = StringField("Name")
    bio = TextAreaField("Bio")
    secret_bio = TextAreaField("Secret Bio")
    game_id = IntegerField("GameID")
    placesubmit = SubmitField("Submit")

class LootForm(FlaskForm):
    name = StringField("Name")
    bio = TextAreaField("Bio")
    copper_value = IntegerField("Copper Value")
    owner_id = IntegerField("Character OwnerID")
    lootsubmit = SubmitField("Submit")

class PlayerForm(FlaskForm):
    users_id = IntegerField("users_id")
    games_id = IntegerField("games_id")
    playersubmit = SubmitField("Submit")

class NoteForm(FlaskForm):
    note = TextAreaField("Live Note")
    private = BooleanField("Private?")
    in_character = BooleanField("In character note?")
    session_number = IntegerField('session number?')
    character = IntegerField('character id')
    charname = StringField("Character name")
    game_id = IntegerField('game id')
    user_id = IntegerField('user_id')
    notesubmit = SubmitField("Submit")

class SessionForm(FlaskForm):
    number = IntegerField("New Session Number", validators=[DataRequired()])
    title = StringField("Session Title", validators=[DataRequired()])
    synopsis = TextAreaField("Quick synopsis of the session")
    games_id = IntegerField("Games_id", validators=[DataRequired()])
    sessionsubmit = SubmitField("Submit")

class NewSessionForm(FlaskForm):
    newsessionsubmit = SubmitField("Start a new Session?")


