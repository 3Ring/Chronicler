from .__init__ import db, socketio
from .classes import *
from flask_socketio import emit
from .helpers import validate as v

# variables
class__buttonEdit = "note_edit_button"
imageLink__defaultCharacter = "/static/images/default_character.jpg"
imageLink__defaultGame = "/static/images/default_game.jpg"
imageLink__defaultDm = "/static/images/default_dm.jpg"
imageLink__buttonEdit = "/static/images/edit_button_image.png"

idPrefix__newSessionHeader = "session_header_"
idPrefix__newSessionCard = "session_card_"
classList__newSessionHeader = ""
classList__newSessionCard = ""

@socketio.on('send_new_session')
def send_new_session(id, number, title, synopsis=None):
    new=Sessions(number=number, title=title, synopsis=synopsis, games_id=id)
    db.session.add(new)
    db.session.flush()
    db.session.commit()

    id__newSessionHeader = idPrefix__newSessionHeader+str(new.id)
    id__newSessionCard = idPrefix__newSessionCard+str(new.number)
    content__newSessionHeader = "Session "+str(new.number)+": "+str(new.title)

    newsession = str(
        "<div id='"
        +id__newSessionHeader
        +"' class='"
        +classList__newSessionHeader
        +"'><h2>"
        +content__newSessionHeader
        +"</h2><div id='"
        +id__newSessionCard
        +"' "
        +classList__newSessionCard
        +"'></div></div>"
    )

    emit('fill_new_session', newsession, broadcast=True)

@socketio.on('send_new_note')
def send_new_note(user_id, game_id, note, priv=False, in_character=False):
    if in_character == 'True':
        in_character = True
    else:
        in_character = False
    if priv == 'True':
        priv = True
    else:
        priv = False

    current_char=Characters.query.filter_by(user_id=user_id, game_id=game_id).first()
    session_number=Sessions.query.with_entities(Sessions.number).filter_by(games_id=game_id).order_by(Sessions.number.desc()).first()[0]
    # this will cause issues if a player has more than one character for now
    new=Notes(charname=current_char.name, note=note, session_number=session_number, private=priv, in_character=in_character, character=current_char.id , user_id=user_id, game_id=game_id)


    db.session.add(new)
    db.session.flush()
    edit_link="<a id='del_"+str(new.id)+"_"+str(new.user_id)+"'><img class='note_edit_button' src='"+imageLink__buttonEdit+"'></a>"
    new_note=str("<span id='note_span_"+str(new.id)+"_"+str(new.user_id)+"'><p id='note"+str(new.id)+"_"+str(new.user_id)+"'>"+str(new.date_added)+" || <b>"+str(new.charname)+":</b> "+str(new.note)+"  "+edit_link+"</p></span>")

    emit('fill_new_note', (new_note, new.private, new.session_number, new.in_character), broadcast=True)
    db.session.commit()

@socketio.on('edit_note')
def edit_note(text, is_private, in_character, game_id, user_id, note_id):
    note = Notes.query.filter_by(id=note_id).first()
    note.note = text
    db.session.flush()
    editted_note=note.note
    emit('fill_note_edit', (editted_note, note.private, note.session_number, note.in_character, note.id), broadcast=True)
    db.session.commit()
    
@socketio.on("delete_note")
def delete_note(id_num):
    note = Notes.query.filter_by(id=id_num).first()
    db.session.delete(note)
    db.session.commit()
    emit('remove_deleted_note', id_num, broadcast=True)

    

