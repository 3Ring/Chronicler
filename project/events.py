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
    edit_link="<a id='del_"+str(new.id)+"_"+new.user_id+"'><img class='edit_button' src='https://image.flaticon.com/icons/png/512/61/61456.png'></a>"
    print('\n\n\n', type(new.id), type(new.user_id), type(new.charname), type(new.date_added), type(new.note))
    new_note=str("<span id='note_span_"+str(new.id)+"_"+new.user_id+"'><p id='note"+str(new.id)+"_"+new.user_id+"'>"+str(new.date_added)+" || <b>"+new.charname+":</b> "+new.note+"  "+edit_link+"</p>")
    emit('fill_new_note', (new_note, new.private, new.session_number, new.in_character), broadcast=True)
    db.session.commit()

