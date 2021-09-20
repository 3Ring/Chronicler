from .classes import *
import base64
from werkzeug.utils import secure_filename
from .events import *
from .classes import *
from . import db
from flask import request

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

def upload(filename):
    print(filename, '\n\n1')
    try:
        pic = request.files[filename]
    except:
        return 'Invalid file or filename'

    if not pic:
        return 'No file uploaded!'

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

    img = Images(img=render_file, name=secure, mimetype=mimetype)
    db.session.add(img)
    db.session.flush()
    id = img.id
    db.session.commit()
    return id 


def nuke():

    db.session.query(Notes).delete()
    print("Notes")
    db.session.commit()

    db.session.query(Sessions).delete()
    print("Sessions")
    db.session.commit()

    db.session.query(Loot).delete()
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

    db.session.query(Players).delete()
    print("Players")
    db.session.commit()

    db.session.query(Games).delete()
    print("Games")
    db.session.commit()

    db.session.query(Images).delete()
    print("Images")
    db.session.commit()

    # db.session.query(Users).delete()
    # print("Users")
    # db.session.commit()

    return


# Functions to dynamically create html elements
# 
# 
# #

def priv_convert(priv):
    if priv == 'True':
        private_ = True
    else:
        private_ = False
    
    return private_

# function to deal with notes' Jinja functions while going through websockets
def note_conditionals(html, model):

    # translate html into a list to insert correct images
    html_list = html.split("\n")
    html = ""
    player_image = '''<div class="author-image" style="background-image: url(../static/images/default_character.jpg)"></div>'''
    dm_image = '''<div class="author-image" style="background-image: url(../static/images/default_dm.jpg)"></div>'''


    # examine each line to remove jinja and insert images at correct locations
    for line in html_list: 
        line = line.strip()
        if model.charname == "DM":
            if line == player_image:
                line = ""
        else:
            if line == dm_image:
                line = ""
        html += line
    return html

# translate note or session into element to send back to client
def translate(model):

    # HTML Templates
    htmlTemplate__newSession = '''
    <div class="session-container">
        <h2>Session {{ session.number }}: {{ session.title }}</h2>
        <div>
            <!-- Session Notes -->
            
            <ul class="note_list" data-idSession="{{ session.number }}">
        </div>
    </div>
    '''

    htmlTemplate__newNote = '''
    <li class="span_cont">
        <span class="span_cont note-item">
            <span class="note-author">

                <div class="author-image" style="background-image: url(../static/images/default_dm.jpg)"></div>

                <div class="author-image" style="background-image: url(../static/images/default_character.jpg)"></div>

                <!-- {{ note.date_added }} || -->
            </span>

            <span class="note-content">
                <h3>{{ note.charname }}:</h3>
                <span class="note-ql" data-id_noteText="{{ note.id }}">
                {{ note.note }}
                </span>
            </span>


            <!-- Edit Button -->
            <a data-editButtonAnchorId="{{ note.id }}" class="edit-note">
                <span data-flag="editButtons" data-id_editImage="{{ note.id }}" class='note_edit_button far fa-edit' src="/static/images/edit_button_image.png"></span>
            </a>
            <form class='hidden edit_form' data-flag="formEdit" data-id_formEdit="{{ note.id }}">
                <input type='text' data-id_formText="{{ note.id }}" value='{{ note.note }}'>
                <input type='submit' value='submit'>
                <span class="checkbox_span">
                    <input type='checkbox' data-id_noteCheckboxPrivate="{{ note.id }}" value='{{ note.private }}'>
                    <label for='change_private_{{ note.id }'>
                        Private?
                    </label>
                </span>
            </form>

            <!-- Edit Note Menu -->
            <div data-contextMenuId="{{ note.id }}" class="note_edit_menu hidden">
                <ul class="note_edit_menu_items">
                    <li class="note_edit_menu_item">
                        <a href="#" data-editMenuId="{{ note.id }}" class="note_edit_menu_link button secondary" data-id_note="{{ note.id }}" data-action="edit">
                            Edit Note
                        </a>
                    </li>
                    <li class="note_edit_menu_item">
                        <a href="#" data-editMenuId="{{ note.id }}" class="note_edit_menu_link button secondary" data-id_note="{{ note.id }}" data-action="delete">
                            Delete Note
                        </a>
                    </li>
                </ul>
            </div>
            
        </span>
    </li>
    
    </ul>
    '''

    # Determine which type of element to create
    header = model.header
    if header == "note.":
        html = htmlTemplate__newNote
        html = note_conditionals(html, model)
    elif header == "session.":
        html = htmlTemplate__newSession
    
    # populate the dict with the model's key/value pairs
    columns = {}
    for column in model.__table__.columns:
        columns[str(column.key)] = getattr(model, str(column.key))

    # iterate through each key/value pair in the model instance's attributes
    for key, value in columns.items():

        # create template for translator
        key = "{{ " + header + key + " }}"

        # replace jinja variables
        html = html.replace(key, str(value))

    return html