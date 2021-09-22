from .__init__ import db, socketio
from .classes import *
from flask_socketio import emit
from .helpers import translate, priv_convert


# variables
class__buttonEdit = "note_edit_button"
imageLink__defaultCharacter = "/static/images/default_character.jpg"\
imageLink__defaultGame = "/static/images/default_game.jpg"
imageLink__defaultDm = "/static/images/default_dm.jpg"
imageLink__buttonEdit = "/static/images/edit_button_image.png"

idPrefix__newSessionHeader = "session_header_"
idPrefix__newSessionCard = "session_card_"

# Create, store and return new session on new session event
@socketio.on('send_new_session')
def send_new_session(games_id, number, title, synopsis=None):

    # convert message to model and add to db
    new=Sessions(number=number, title=title, synopsis=synopsis, games_id=games_id)
    db.session.add(new)
    db.session.flush()
    db.session.commit()

    # convert data to html element
    elements = translate(new)
    session_container = elements[0]
    session_list = elements[1]
    # return data to client
    emit('fill_new_session', (session_container, session_list, str(number)), broadcast=True)


@socketio.on('send_new_note')
def send_new_note(user_id, game_id, session_number, note, private_=False):

    private_ = priv_convert(private_)
    
    current_char=Characters.query.filter_by(user_id=user_id, game_id=game_id).first()
    session_number=session_number

    # this will cause issues if a player has more than one character for now
    new=Notes(charname=current_char.name, session_number=session_number, note=note, private=private_, in_character=False, character=current_char.id , user_id=user_id, game_id=game_id)

    db.session.add(new)
    db.session.flush()
    db.session.commit()

    # convert data to html element
    element = translate(new)[0]

    emit('fill_new_note', (element, new.private, new.id, new.session_number), broadcast=True)
    

@socketio.on('edit_note')
def edit_note(text, is_private, game_id, user_id, note_id):
    private = priv_convert(is_private)
    note = Notes.query.filter_by(id=note_id).first()
    note.note = text
    note.private = private
    db.session.flush()
    db.session.commit()

    editted_note= translate(note)[0]
    emit('fill_note_edit', (editted_note, private, note.session_number, note.id), broadcast=True)
    
    
@socketio.on("delete_note")
def delete_note(id_num):
    note = Notes.query.filter_by(id=id_num).first()
    db.session.delete(note)
    db.session.commit()
    emit('remove_deleted_note', id_num, broadcast=True)

    

