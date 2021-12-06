import os
import base64
from werkzeug.utils import secure_filename

from project.models import *
from project.__init__ import db
from werkzeug.security import generate_password_hash
from flask import request


# def allowed_file(filename):
# ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
# for i, letter in enumerate(filename):
#     if letter == '/':
#         altered = (filename[i+1:]).lower()
#         break

# if altered in ALLOWED_EXTENSIONS:
#     return True
# return False

# def render_picture(data):

#     render_pic = base64.b64encode(data).decode('ascii')
#     return render_pic

# def upload(filename, testing=False):
# try:
#     pic = request.files[filename]
# except:
#     return 'Invalid file or filename'

# if not pic:
#     return -1

# if len(pic.stream.read()) > 3000000:
#     return 'image is too large. limit to images 1MB or less.'

# mimetype = pic.mimetype
# if not allowed_file(mimetype):
#     return "Not allowed file type. Image must be of type: .png .jpg or .jpeg"

# secure = secure_filename(pic.filename)

# if not secure or not mimetype:
#     return 'Bad upload!'

# pic.stream.seek(0)
# data = pic.stream.read()
# render_file = render_picture(data)

# img = Images(img=render_file, name=secure, mimetype=mimetype)
# db.session.add(img)
# db.session.flush()
# _id = img.id
# if testing != False:
#     db.session.commit()
# return _id


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


# Functions to dynamically create html elements
#
#
# #


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


# # function to deal with notes' Jinja functions while going through websockets
# def note_conditionals(html, model):

#     # translate html into a list to insert correct images
#     html_list = html.split("\n")
#     html = ""
#     player_image = '''<div class="author-image" style="background-image: url(../static/images/default_character.jpg)"></div>'''
#     dm_image = '''<div class="author-image" style="background-image: url(../static/images/default_dm.jpg)"></div>'''


#     # examine each line to remove jinja and insert images at correct locations
#     for line in html_list:
#         line = line.strip()
#         if model.charname == "DM":
#             if line == player_image:
#                 line = ""
#         else:
#             if line == dm_image:
#                 line = ""
#         html += line
#     return html

# # translate note or session into element to send back to client
# def translate(model):

#     # HTML Templates
#     htmlTemplate__newSession = '''
#     <div class="session-container hidden" data-flag="session_cont" data-number_sessionCont="{{ session.number }}">
#         <h2>Session {{ session.number }}: {{ session.title }}</h2>
#         <div>
#             <!-- Session Notes -->
#             <ul class="note_list" data-idSession="{{ session.number }}">
#         </div>
#     </div>
#     '''

#     htmlTemplate__newSessionList = '''
#     <li class="session-anchor current" data-flag="sessionList" data-number_sessionList="{{ session.number }}">
#         <h4>Session {{ session.number }}</h4>
#         <h2>{{ session.title }}</h2>
#     </li>
#     '''
#     htmlTemplate__newNote = '''
#     <li class="span_cont" data-id_noteCont="{{ note.id }}">
#         <span class="span_cont note-item">
#             <span class="note-author">

#                 <div class="author-image" style="background-image: url(../static/images/default_dm.jpg)"></div>

#                 <div class="author-image" style="background-image: url(../static/images/default_character.jpg)"></div>
#                 <!-- {{ note.date_added }} || -->
#             </span>

#             <span class="note-content">
#                 <h3>{{ note.charname }}:</h3>
#                 <span class="note-ql" data-id_noteText="{{ note.id }}">
#                 {{ note.note }}
#                 </span>
#             </span>


#             <!-- Edit Button -->
#             <a data-editButtonAnchorId="{{ note.id }}" class="edit-note">
#                 <span data-flag="editButtons" data-id_editImage="{{ note.id }}" class='note_edit_button far fa-edit' src="/static/images/edit_button_image.png"></span>
#             </a>

#         </span>

#             <form class="hidden wysiwyg-form" data-flag="formEdit" data-id_formEdit="{{ note.id }}">
#                 <div class="form-group" >

#                     <input type="hidden" id='note_user_id' name='note_user_id' value='{{ note.user_id }}'>
#                     <input type="hidden" id='note_game_id' name='note_game_id' value='{{ note.game_id }}'>
#                     <div id="QuillEdit_{{ note.id }}" data-crumb="{{ note.id }}">
#                     </div>
#                 </div>
#                 <div class="form-group">
#                     <div class="row checkbox">
#                         <input type='checkbox' class="note_checkbox" data-id_noteCheckboxPrivate="{{ note.id }}" name='note_private' value='False'>
#                         <label for='note_private'>Private - Visible only to you and the DM.</label>
#                     </div>
#                     <div class="row button-row">
#                         <button class="button primary" type="submit">Submit</button>
#                     </div>
#                 </div>
#             </form>

#             <!-- Edit Note Menu -->
#             <div data-contextMenuId="{{ note.id }}" data-flag="contextMenu" class="note_edit_menu hidden">
#                 <ul class="note_edit_menu_items">
#                     <li class="note_edit_menu_item">
#                         <a href="#" data-editMenuId="{{ note.id }}" class="note_edit_menu_link button primary" data-id_note="{{ note.id }}" data-action="edit">
#                             Edit Note
#                         </a>
#                     </li>
#                     <li class="note_edit_menu_item">
#                         <a href="#" data-editMenuId="{{ note.id }}" class="note_edit_menu_link button primary" data-id_note="{{ note.id }}" data-action="delete">
#                             Delete Note
#                         </a>
#                     </li>
#                 </ul>
#             </div>
#     </li>
#     '''

#     # Determine which type of element to create
#     header = model.header
#     if header == "note.":
#         html = htmlTemplate__newNote
#         html = note_conditionals(html, model)
#         html = [html]
#     elif header == "session.":
#         html = [htmlTemplate__newSession, htmlTemplate__newSessionList]

#     # populate the dict with the model's key/value pairs
#     columns = {}
#     for column in model.__table__.columns:
#         columns[str(column.key)] = getattr(model, str(column.key))

#     # iterate through each key/value pair in the model instance's attributes
#     i = 0
#     while i < len(html):
#         for key, value in columns.items():

#             # create template for translator
#             key = "{{ " + header + key + " }}"

#             # replace jinja variables
#             html[i] = html[i].replace(key, str(value))
#         i+=1

#     return html

# # function to be run on server init
# # run on db creation for tutorial messages
# def init_training_wheels_db():
#     admin_pass = os.environ.get("ADMIN_PASS")
#     chronicler_user = Users(name = "Chronicler", email="app@chronicler.gg", hash=generate_password_hash(admin_pass, method='sha256'))
#     db.session.add(chronicler_user)
#     db.session.commit()
#     new = Users.query.filter_by(id=chronicler_user.id).first()
#     print(f"{new.name} added to the db!")


# def new_game_training_wheels(game):
#     """add tutorial notes and session zero to game"""

#     tutorial_user=Users.query.filter_by(email="app@chronicler.gg").first()
#     # add tutorial character
#     tutorial_character = Characters(name="Chronicler Helper", user_id=tutorial_user.id, game_id=game.id)
#     db.session.add(tutorial_character)
#     db.session.commit()

#     # add session zero
#     session_zero = Sessions(number=0, title="The Adventure Begins!", games_id=game.id)
#     db.session.add(session_zero)
#     db.session.commit()

#     tutorial_notes = []
#     note_texts = [
#         # note 1
#         '''
#         <p><strong class="ql-size-huge"><u>Intro Note 1:</u></strong></p><p>Welcome to your next great adventure!</p><p><br></p><p>This is a place where you can write and share notes.</p>
#         ''',
#         # note 2
#         '''
#         <p><strong class="ql-size-huge"><u>Intro Note 2:</u></strong></p><p>Notes are ordered by "Session" by which we typically mean game session, but for you it can mean whatever you want!</p><p><br></p><p>For your "Session Zero" notes I recommend you have notes related to the overall shape of your game. A short list would be:</p><p><br></p><ol><li>house rules</li><li>areas of roleplay and story that are off limits due to player comfort</li><li>expectations</li></ol><ul><li>how long each session should be</li><li>how often you plan to meet</li><li>what you will do if a player can't make it</li><li>etc!</li></ul>
#         ''',
#         # note 3
#         '''
#         <p><strong class="ql-size-huge"><u>Intro Note 3:</u></strong></p><p>you can edit and delete your notes whenever you like, and though you can't typically delete other player's note, you are more than welcome to get rid of mine if you are already experts!</p>
#         ''',
#         # note 4
#         '''
#         <p><strong class="ql-size-huge"><u>Intro note 4:</u></strong></p><p>Right now this site is in an Alpha phase, which means Chronicler is just a baby!</p><p><br></p><p>If you notice anything that seems broken or could be improved please let me know so I can make it better!</p>
#         ''',
#         # note 5
#         '''
#         <p><strong class="ql-size-huge"><u>Intro Note 5:</u></strong></p><p>This is the last note in the session!</p><p><br></p><p><em>Then why is it at the top?</em></p><p><br></p><p>Chronicler is designed to be a collaborative note taking application. That means that it's meant to be used while you are playing together! We think it's better if the newest notes appear at the top of the page.</p><p><br></p><p>Don't worry, you can change this if you like....<strong>(eventually)</strong></p>
#         '''
#     ]

#     for note in note_texts:
#         tutorial_notes.append(Notes(charname="Chronicler Helper", note=note, session_number=0, user_id=tutorial_user.id, character=tutorial_character.id, game_id=game.id))

#     for Note_obj in tutorial_notes:
#         db.session.add(Note_obj)
#         db.session.commit()


def make_character_images(character_id):
    character = Characters.query.filter_by(id=character_id).first()
    image = Images.query.filter_by(id=character.img_id).first()
    # set defaults if no image exists

    if image == None:
        if character.name == "DM":
            return "/static/images/default_dm.jpg"
        else:
            return "/static/images/default_character.jpg"
    else:
        decoder2 = f"data:{image.mimetype};base64, "
        return decoder2 + image.img
