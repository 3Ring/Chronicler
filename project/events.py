from .__init__ import db, socketio
from .classes import *
from flask_socketio import emit
from .helpers import make_character_images, translate, priv_convert
from .socket_helper import translate_jinja

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
def send_new_session(games_id, number, title, synopsis=None):

    # convert message to model and add to db
    new=Sessions(number=number, title=title, synopsis=synopsis, games_id=games_id)
    db.session.add(new)
    db.session.flush()
    db.session.commit()

    # convert data to html element
    elements = translate_jinja(new, "session", games_id)

    # return data to client
    emit('fill_new_session', (elements["card"], elements["nav"], str(number)), broadcast=True)


@socketio.on('send_new_note')
def send_new_note(user_id, game_id, session_number, note, priv=False, to_gm=False):

    private2 = priv_convert(priv)
    to_gm = priv_convert(to_gm)
    dm_id = Games.query.filter_by(id = game_id).first().id
    
    current_char=Characters.query.filter_by(user_id=user_id, game_id=game_id).first()
    char_img = make_character_images(current_char.id)
    session_number=session_number

    # this will cause issues if a player has more than one character for now
    new=Notes(charname=current_char.name, session_number=session_number, note=note, private=private2, to_gm=to_gm, character=current_char.id , user_id=user_id, game_id=game_id)
    new.char_img = char_img
    db.session.add(new)
    db.session.flush()
    # db.session.commit()

    # convert data to html element
    element = translate_jinja(new, "note", game_id, u_id=new.user_id, d_id=dm_id, char_img=char_img)
    # print(f" returned element: {element}")
    # print(new.user_id, new.private, new.to_gm, new.id, new.session_number)
    # print(private2, new.private)
    emit('fill_new_note', (element["no_sections"], new.note, new.private, new.to_gm, new.id, new.session_number), broadcast=True)
    

@socketio.on('edit_note')
def edit_note(text, is_private, game_id, user_id, note_id):
    private = priv_convert(is_private)
    note = Notes.query.filter_by(id=note_id).first()
    dm_id = Games.query.filter_by(id = game_id).first().id
    current_char=Characters.query.filter_by(user_id=user_id, game_id=game_id).first()
    char_img = make_character_images(current_char.id)
    note.note = text
    note.private = private
    note.char_img = char_img

    db.session.flush()
    db.session.commit()

    editted_note= translate_jinja(note, "note", game_id, u_id=user_id, d_id=dm_id, char_img=char_img)
    emit('fill_note_edit', (editted_note, private, note.session_number, note.id), broadcast=True)
    
    
@socketio.on("delete_note")
def delete_note(id_num):
    note = Notes.query.filter_by(id=id_num).first()
    db.session.delete(note)
    db.session.commit()
    emit('remove_deleted_note', id_num, broadcast=True)
 
    

