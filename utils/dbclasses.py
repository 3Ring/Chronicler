from sqlalchemy.orm import backref
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask

# # Configure application
# app = Flask(__name__)

# # Setting up MYSQL database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/BON'
# # Secret Key
# app.config['SECRET_KEY'] = 'is it secret?'
# # Initialize the database
# db = SQLAlchemy(app)

# Configure application
app = Flask(__name__)

# old SQLitedb
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///liteBON.db'
# Setting up MYSQL database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/BON'
# Secret Key
app.config['SECRET_KEY'] = 'is it secret?'
# Initialize the database
db = SQLAlchemy(app)

# Create Models for db
# Players
players = db.Table('players',
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True),
    db.Column('games_id', db.Integer, db.ForeignKey('games.id'), nullable=False, primary_key=True)
)

# Users
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    hash = db.Column(db.String(120), nullable=False)
    realname = db.Column(db.String(20))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    characters = db.relationship('Characters', backref='user', lazy=True)

    # Create A String
    def __repr__(self):
        return '<User %r>' % self.username

# Games
class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    imglink = db.Column(db.String(200), nullable=False)
    sessions = db.Column(db.Integer, nullable=False)
    secret = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    dm_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    places = db.relationship('Places', backref='game', lazy=True)
    NPCs = db.relationship('NPCs', backref='game', lazy=True)
    # PCs = db.relationship('Characers', backref='game', lazy=True)

    players = db.relationship('Users', secondary=players, lazy='subquery',
        backref=db.backref('games', lazy=True))

    # Create A String
    def __repr__(self):
        return '<Game %r>' % self.name

# Characters
class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    imglink = db.Column(db.String(200))
    bio = db.Column(db.Text)
    platinum = db.Column(db.Integer, default=0)
    gold = db.Column(db.Integer, default=0)
    electrum = db.Column(db.Integer, default=0)
    siver = db.Column(db.Integer, default=0)
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

    # Create A String
    def __repr__(self):
        return '<Character %r>' % self.name

# NPCs
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

    # Create A String
    def __repr__(self):
        return '<NPC %r>' % self.name

# Places
class Places(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    bio = db.Column(db.Text, default='A Place of Mystery')
    secret_bio = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    NPCs = db.relationship('NPCs', backref='place', lazy=True)

    # Create A String
    def __repr__(self):
        return '<Place %r>' % self.name

# loot
class loot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    bio = db.Column(db.Text, default='An item shrouded in mystery')
    copper_value = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

    # Create A String
    def __repr__(self):
        return '<Loot %r>' % self.name
