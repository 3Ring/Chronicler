from .__init__ import db, socketio
from .classes import *
from flask_socketio import emit
from .helpers import validate as v
from .helpers import element_builder, Blueprint_reader, priv_convert


# variables
class__buttonEdit = "note_edit_button"
imageLink__defaultCharacter = "/static/images/default_character.jpg"
imageLink__defaultGame = "/static/images/default_game.jpg"
imageLink__defaultDm = "/static/images/default_dm.jpg"
imageLink__buttonEdit = "/static/images/edit_button_image.png"

idPrefix__newSessionHeader = "session_header_"
idPrefix__newSessionCard = "session_card_"

# Create, store and return new session on new session event
@socketio.on('send_new_session')
def send_new_session(id, number, title, synopsis=None):

    # convert message to model and add to db
    new=Sessions(number=number, title=title, synopsis=synopsis, games_id=id)
    db.session.add(new)
    db.session.flush()
    db.session.commit()

    # convert data to html element
    template = Blueprint_reader("newsession", new)
    element = element_builder(template)

    # return data to client
    emit('fill_new_session', element, broadcast=True)


@socketio.on('send_new_note')
def send_new_note(user_id, game_id, note, priv=False):
    
    priv_convert(priv)

    current_char=Characters.query.filter_by(user_id=user_id, game_id=game_id).first()
    session_number=Sessions.query.with_entities(Sessions.number).filter_by(games_id=game_id).order_by(Sessions.number.desc()).first()[0]
    # this will cause issues if a player has more than one character for now
    new=Notes(charname=current_char.name, note=note, session_number=session_number, private=priv, in_character=False, character=current_char.id , user_id=user_id, game_id=game_id)


    db.session.add(new)
    # db.session.flush()
    # db.session.commit()

    # convert data to html element
    template = Blueprint_reader("newnote", new)
    element = element_builder(template)

    edit_link="<a id='del_"+str(new.id)+"_"+str(new.user_id)+"'><img class='note_edit_button' src='"+imageLink__buttonEdit+"'></a>"
    new_note=str("<span id='note_span_"+str(new.id)+"_"+str(new.user_id)+"'><p id='note"+str(new.id)+"_"+str(new.user_id)+"'>"+str(new.date_added)+" || <b>"+str(new.charname)+":</b> "+str(new.note)+"  "+edit_link+"</p></span>")

    emit('fill_new_note', (new_note, new.private, new.session_number), broadcast=True)
    

@socketio.on('edit_note')
def edit_note(text, is_private, game_id, user_id, note_id):
    note = Notes.query.filter_by(id=note_id).first()
    note.note = text
    note.private = is_private
    db.session.flush()
    editted_note=note.note
    emit('fill_note_edit', (editted_note, note.private, note.session_number, note.id), broadcast=True)
    db.session.commit()
    
@socketio.on("delete_note")
def delete_note(id_num):
    note = Notes.query.filter_by(id=id_num).first()
    db.session.delete(note)
    db.session.commit()
    emit('remove_deleted_note', id_num, broadcast=True)

    

