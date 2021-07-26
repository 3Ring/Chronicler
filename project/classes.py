from sqlalchemy.orm import backref
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
from flask_login import UserMixin
from .__init__ import db



class Players(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    games_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)

    head = [
        'id',
        'users_id',
        'games_id'
    ]

    def __repr__(self):
        return '< Player: %r >' % self



# Create Models for db
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    hash = db.Column(db.String(120), nullable=False)
    realname = db.Column(db.String(20))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    characters = db.relationship('Characters', backref='user', lazy=True)

    head =[
        'ID', 
        'User Name', 
        'Email', 
        'Hash', 
        'Real Name', 
        'Date Added',
        'Characters']

    def __repr__(self):
        return '< User.id: %r >' % self.id

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    imglink = db.Column(db.String(200), nullable=False)
    sessions = db.Column(db.Integer, nullable=False)
    secret = db.Column(db.Integer, default=0)
    published = db.Column(db.Boolean, default=False, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    dm_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    places = db.relationship('Places', backref='game', lazy=True)
    NPCs = db.relationship('NPCs', backref='game', lazy=True)


    players = db.relationship('Users', secondary='players', lazy='subquery',
        backref=db.backref('games', lazy=True))

    head = [
        'ID', 
        'Name', 
        'Imglink', 
        'Sessions', 
        'Secret', 
        'Date Added', 
        'DM ID',
        'Players']

    def __repr__(self):
        return '<Game %r>' % self.name

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    charname=db.Column(db.String(50))
    note = db.Column(db.Text)
    session_id = db.Column(db.Integer)
    private = db.Column(db.Boolean)
    in_character = db.Column(db.Boolean)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    character = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)

    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    head = [
        'ID',
        'Note',
        'session_id',
        'Private',
        'In Character',
        'date_added',
        'character',
        'game_id'
    ]

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    imglink = db.Column(db.String(200))
    bio = db.Column(db.Text)
    platinum = db.Column(db.Integer, default=0)
    gold = db.Column(db.Integer, default=0)
    electrum = db.Column(db.Integer, default=0)
    silver = db.Column(db.Integer, default=0)
    copper = db.Column(db.Integer, default=0)
    experience = db.Column(db.Integer, default=0)
    strength = db.Column(db.Integer, default=0)
    dexterity = db.Column(db.Integer, default=0)
    constitution = db.Column(db.Integer, default=0)
    intelligence = db.Column(db.Integer, default=0)
    wisdom = db.Column(db.Integer, default=0)
    charisma = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)

    # items = db.relationship('Loot', backref='character', lazy=True)

    head = [
    'ID', 
    'Name', 
    'ImgLink', 
    'Bio', 
    'PP', 
    'GP', 
    'EP', 
    'SP', 
    'CP', 
    'XP', 
    'STR', 
    'DEX', 
    'CON', 
    'INT', 
    'WIS', 
    'CHA', 
    'Date Added', 
    'User ID', 
    'Game ID']

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

    # loot = db.relationship('Loot', backref='NPC', lazy=True)

    head = [
        'ID',
        'Name',
        'Secret Name',
        'Bio',
        'Secret Bio',
        'Date Added',
        'Game ID',
        'Place ID'
    ]

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

    head = [
        'ID',
        'Name',
        'Bio',
        'Secret Bio',
        'Date Added',
        'Game ID',
        'NPCs'
    ]

    def __repr__(self):
        return '<Place %r>' % self.name

class Loot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    bio = db.Column(db.Text, default='An item shrouded in mystery')
    copper_value = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

    head = [
        'ID',
        'Name',
        'Bio',
        'Value(CP)',
        'Date Added',
        'Owner ID'
    ]

    def __repr__(self):
        return '<Loot %r>' % self.name






# Form models
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    hash = StringField("Password", validators=[DataRequired ()])
    realname = StringField("Real Name")
    usersubmit = SubmitField("Submit")

class LoginForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired ()])
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
    submit = SubmitField("Submit")

class ConForm(FlaskForm):
    todelete = StringField("Item to Delete:")
    confirm = SubmitField("Confirm")
    cancel = SubmitField("Cancel")

class GameForm(FlaskForm):
    name = StringField("Name")
    imglink = TextAreaField("Image Link")
    sessions = IntegerField("Number of Sessions")
    secret = IntegerField("User who this game is attached to '0' if published")
    published = BooleanField("Publish? (Allow game to be searchable)")
    dm_id = IntegerField("User_id who this game is attached to")
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
    imglink = TextAreaField("Image Link")
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
    session = IntegerField('session?')
    character = IntegerField('character id')
    game = IntegerField('game id')
    remember = BooleanField("Remember Me")
    notesubmit = SubmitField("Submit")

