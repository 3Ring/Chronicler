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
    newsession = str("<div id='session_header_"+str(new.id)+"'>Session"+str(new.number)+": "+str(new.title)+"<div id='session_card_"+str(new.number)+"'></div></div>")
    emit('fill_new_session', newsession, broadcast=True)

@socketio.on('send_new_note')
def send_new_note(user_id, game_id, note, private=False, in_character=False):
    if in_character == 'y':
        in_character = True
    else:
        in_character = False
    if private == 'y':
        private = True
    else:
        private = False

    current_char=Characters.query.filter_by(user_id=user_id, game_id=game_id).first()
    session_number=Sessions.query.with_entities(Sessions.number).filter_by(games_id=game_id).order_by(Sessions.number.desc()).first()[0]
    # this will cause issues if a player has more than one character for now
    new=Notes(charname=current_char.name, note=note, session_number=session_number, private=private, in_character=in_character, character=current_char.id , user_id=user_id, game_id=game_id)
    
    db.session.add(new)
    db.session.flush()
    new_note=str("<p id='note"+str(new.id)+"'>"+str(new.charname)+":  "+str(new.note)+"</p>")
    emit('fill_new_note', (new_note, new.private, new.session_number, new.in_character), broadcast=True)
    db.session.commit()

