from .classes import *
import base64
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
from .events import *
from .classes import *
from flask_login import login_required, current_user
from . import db
def validate(var, name="NoName", deep=False):
    it=0
    strit=str(it)
    print((it+1)*5*'{0}'.format(it), '<><><><>', (50-it)*'{0}'.format(it))
    print('\n', name, ': ', '<'+strit+'<'+strit+'<'+strit+'<', var, '>'+strit+'>'+strit+'>'+strit+'>', '\n', 'Is type: ', type(var), '\n')
    print(10*('-'+strit)+'-')
    if deep == True:
        try:
            if len(var) > 1:
                it+=1
                strit=str(it)
                print((it+1)*3*'{0}'.format(it), '<><><><>', (30-it)*'{0}'.format(it))
                for item in var:
                    try:
                        if len(item) > 1:
                            validate(item, "recur-item<{0}>".format(it), it)
                    except:
                        print('\n', name, ': ', '<'+strit+'<'+strit+'<'+strit+'<', item, '>'+strit+'>'+strit+'>'+strit+'>', '\n', 'Is type: ', type(item), '\n')
            
            return None
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            return None


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def upload(filename):
    pic = request.files[filename]
    print('number 2')
    if not pic:
        return 'No file uploaded!'

    if not allowed_file(pic.filename):
        return "Not allowed file type. Image must be of type: .png .jpg or .jpeg"

    secure = secure_filename(pic.filename)
    print("secure", secure)
    mimetype = pic.mimetype
    print("mimetype", mimetype)
    if not secure or not mimetype:
        return 'Bad upload!'

    img = Images(img=base64.b64encode(pic.read()), name=secure, mimetype=mimetype)
    print(img.img)
    db.session.add(img)
    db.session.flush()
    id = img.id
    db.session.commit()
    print("id: ", id)
    return id


def nuke(count=0):
    count += 1
    nope = 0
    try:
        db.session.query(Notes).delete()
    except:
        print("Notes")
        nope = 1
    try:
        db.session.query(Loot).delete()
    except:
        nope = 1
        print("Loot")
    try:
        db.session.query(Places).delete()
    except:
        nope = 1
        print("Places")
    try:
        db.session.query(NPCs).delete()
    except:
        nope = 1
        print("NPCs")
    try:
        db.session.query(Characters).delete()
    except:
        nope = 1
        print("Characters")
    try:
        db.session.query(Sessions).delete()
    except:
        nope = 1
        print("Sessions")
    try:
        db.session.query(Games).delete()
    except:
        nope = 1
        print("Games")
    try:
        db.session.query(Users).delete()
    except:
        nope = 1
        print("Users")
    try:
        db.session.query(Players).delete()
    except:
        nope = 1
        print("Players")
    try:
        db.session.query(Images).filter(Images.id != 1 or Images.id != 2 or Images.id != 3).delete()
    except:
        nope = 1
        print("Players")
    db.session.commit()
    if nope == 1:
        nuke()
    if count == 20:
        return count
    return count