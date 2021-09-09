from .__init__ import db, socketio
from .classes import *
from flask_socketio import emit
from .helpers import validate as v

@socketio.on('send_new_session')
def send_new_session(id, number, title, synopsis=None):
    new=Sessions(number=number, title=title, synopsis=synopsis, games_id=id)
    db.session.add(new)
    db.session.flush()
    db.session.commit()
    newsession = str("<div class='border shadow-lg p-3 mb-5 bg-light rounded' id='session_header_"+str(new.id)+"'><h2>Session "+str(new.number)+": "+str(new.title)+"</h2><div id='session_card_"+str(new.number)+"'></div></div>")
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
    edit_link="<a id='del_"+str(new.id)+"_"+str(new.user_id)+"'><img class='note_edit_button' src='https://image.flaticon.com/icons/png/512/61/61456.png'></a>"
    new_note=str("<span id='note_span_"+str(new.id)+"_"+str(new.user_id)+"'><p id='note"+str(new.id)+"_"+str(new.user_id)+"'>"+str(new.date_added)+" || <b>"+str(new.charname)+":</b> "+str(new.note)+"  "+edit_link+"</p></span>")

    emit('fill_new_note', (new_note, new.private, new.session_number, new.in_character), broadcast=True)
    db.session.commit()

@socketio.on('edit_note')
def edit_note(text, is_private, in_character, game_id, user_id, note_id):
    # print('edit_note received!!', text, is_private, in_character, game_id, user_id, note_id)
    note = Notes.query.filter_by(id=note_id).first()
    note.note = text
    db.session.flush()
    editted_note=note.note
    emit('fill_note_edit', (editted_note, note.private, note.session_number, note.in_character, note.id), broadcast=True)
    db.session.commit()
    
@socketio.on("delete_note")
def delete_note(id_num):
    # print("delete_note", id_num)
    note = Notes.query.filter_by(id=id_num).first()
    db.session.delete(note)
    db.session.commit()
    emit('remove_deleted_note', id_num, broadcast=True)

    

