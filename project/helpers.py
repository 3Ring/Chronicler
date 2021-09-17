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


# builds each element from a dictionary
def make_element(**dictionary):
    element = ""
    # add sibling element
    if "beforeBegin" in dictionary.keys():
        element += dictionary["beforeBegin"]

    # add HTML opening tag
    element += "<"
    if "type" in dictionary.keys():
        element += dictionary["type"]
    else:
        return 1

    # add classes to element if they exist
    if "class" in dictionary.keys():
        element += " class='"
        element += dictionary["class"]
        element += "'"

    # add classes to element if they exist
    if "style" in dictionary.keys():
        element += " style='"
        element += dictionary["style"]
        element += "'"

    # add "data-<type>" to element if it exists
    if "dataType" in dictionary.keys():
        element += " data-"
        element += dictionary["dataType"]
        element += "='"
        
        # if the data type has a value add it
        if "dataValue" in dictionary.keys():
            element += dictionary["dataValue"]
        element += "'"
    element += ">"

    # add innerHTML 1st sibling if it exists
    if "afterBegin" in dictionary.keys():
        element += dictionary["afterBegin"]
    
    # add innerHTML if it exists
    if "innerHTML" in dictionary.keys():
        element += dictionary["innerHTML"]

    # add childElement if it exists
    if "childElement" in dictionary.keys():
        element += dictionary["childElement"]

    # add innerHTML 2nd sibling if it exists
    if "beforeEnd" in dictionary.keys():
        element += dictionary["beforeEnd"]

    # Close tag
    element += "</"
    element += dictionary["type"]
    element += ">"

    # Add folloing element if it exists
    if "afterEnd" in dictionary.keys():
        element += dictionary["afterEnd"]
    print(element)
    return element


# nests all the elements together into one
# elements need to be ordered child -> parent (optional sibling)-> grandparent
# siblings are optional at any step
def element_builder( element_list ):
    complete_element = ""

    # nest each element
    for element in element_list:

        # if the incoming element isn't a parent element it returns sibling elements
        if "sibling" in element.keys():
            element[ "afterEnd" ] = complete_element
        elif "step_sibling" in element.keys():
            element[ "beforeBegin" ] = complete_element
        else:
            element[ "childElement" ] = complete_element

        complete_element = make_element( **element )

        # error(s)
        if type(complete_element) is int:
            if complete_element == 1:
                raise "dictionary missing element type"

    return complete_element

def Blueprint_reader(style, model, user_id=None):
    # dictionary HTML element blueprints
    newSession = [
            {
                "type": "div"
                , "class": "session-container"
            }
            , {
                "type": "h2"
                , "sibling": True
            }
            , {
                "type": "div"
            }
            , {
                "type": "ul"
                , "class": "note_list"
                , "dataType": "idSession"
            }
    ]
    newnote_author = [
        {
            "type": "span"
            , "class": "note-author"
        }
        , {
            "type": "div"
            ,"class": "author-image"
        }
    ]
    newnote_content = [
        {
            "type": "span"
            , "class": "note-content"
            , "sibling": True
        }
        , {
            "type": "h3"
            , "sibling": True
        }
        , {
            "type": "span"
            , "class": "note-ql"
            , "dataType": "noteText"
            , "sibling": True
        }
    ]
    newnote = [
        {
            "type": "li"
            , "class": "span_cont"
        }
        , {
            "type": "span"
            , "class": "span_cont note-item"
        }
    ]



    if style == "newsession":
        newSession[1]['innerHTML'] = "Session"+str(model.number)+": "+model.title
        newSession[1]['dataValue'] = str(model.number)
        newSession.reverse()
        return newSession
    elif style == "newnote_author":
        if model.charname == "DM":
            newnote_author[1]["style"] = "background-image: url(../static/images/default_character.jpg)"
        else:
            newnote_author[1]["style"] = "background-image: url(../static/images/default_dm.jpg)"
        # newnote_content.reverse()
        return newnote_author
    elif style == "newnote_content":
        newnote_content[1]["innerHTML"] = model.charname+":"
        newnote_content[2]["dataValue"] = str(model.id)
        # newnote_content.reverse()
        return newnote_content
    elif style == "newnote_editbutton":
        # todo
        return
    elif style == "newnote_editform":
        # todo
        return
    elif style == "newnote_editnotemenu":
        # todo
        return
    elif style == "newnote_editform_edit":
        # todo
        return
    elif style == "newnote_editform_delete":
        # todo
        return
    elif style == "newnote":
        author_template = Blueprint_reader("newnote_author", model, user_id)
        # author_element =  element_builder(author_template)
        content_template = Blueprint_reader("newnote_content", model, user_id)
        # content_element = element_builder(content_template)
        
        newnote = content_template + author_template + newnote
        newnote.reverse()
        return newnote
    else:
        print("no")
        raise "incorrect style"

def priv_convert(priv):
    if priv == 'True':
        private_ = True
    else:
        private_ = False
    
    return private_
