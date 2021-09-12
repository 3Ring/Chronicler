from .classes import *
import base64
from werkzeug.utils import secure_filename
from .events import *
from .classes import *
from . import db
from flask import request


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