from . import db, socketio
from .classes import *
from flask_socketio import send, emit

def called():
    print('\n\n\n\n', 'received', '\n\n\n\n')

@socketio.on('send_new_session')
def send_new_session(id, number, title, synopsis=None):

    print('\n\n\n\n', 'send_new_session', id, number, title, '\n\n\n\n')
    new=Sessions(number=number, title=title, synopsis=synopsis, games_id=id)
    db.session.add(new)
    db.session.flush()
    db.session.commit()
    newsession = str("<div id='session"+str(new.number)+"'>Session"+str(new.number)+": "+new.title+"</div")
    print('\n\n\n\n', str("<div id='session"+str(new.number)+"'></div"), '\n\n\n\n')
    emit('fill_new_session', newsession, broadcast=True)

@socketio.on('send_new_note')
def send_new_note(user_id, game_id, note, private=False, in_character=False):
    if in_character == 'true':
        in_character = True
    else:
        in_character = False
    if private == 'true':
        private = True
    else:
        private = False
    print('\n\n\n\n', 'send_new_note', user_id, game_id, note, private, in_character, '\n\n\n\n')
    charname=Characters.query.with_entities(Characters.name).filter_by(user_id=user_id).first()
    print('\n\n\n\n', 'charname', charname)
    session_id=Sessions.query.with_entities(Sessions.id).filter_by(games_id=game_id).order_by(Sessions.id.desc()).first()
    print('\n\n\n\n', 'session_id:', session_id)
    # this will cause issues if a player has more than one character for now
    character=Characters.query.with_entities(Characters.id).filter_by(user_id=user_id).first()
    print('\n\n\n\n', "character:", character)
    print('\n\n\n\n', "game_id:", game_id)

    new=Notes(charname=charname[0], note=note, session_id=session_id[0], private=private, in_character=in_character, character=character[0], game_id=game_id)
    
    db.session.add(new)
    db.session.flush()
    new_note=str("<div id='note"+str(new.id)+"'>"+str(new.charname)+":  "+str(new.note)+"</div>")
    print('\n\n\n\n', new.session_id)
    emit('fill_new_note', (new_note, new.private, new.session_id, new.in_character), broadcast=True)
    db.session.rollback()




# tests below here
@socketio.on('pushnote')
def pushtest(test, id):

    print('\n\n\n', 'id: ', id, '  test:   ', test, '\n\n\n')
    new=Test(test=test)
    db.session.add(new)
    db.session.flush()
    db.session.commit()
    new = str('<li>'+id+": "+test+'</li>')
    emit('fill', new)

# test
@socketio.on('pushtest')
def pushtest(test, id):
    print('\n\n\n', 'id: ', id, '  test:   ', test, '\n\n\n')
    new=Test(test=test)
    db.session.add(new)
    db.session.flush()
    db.session.commit()
    new = str('<li>'+id+": "+test+'</li>')
    emit('filltest', new)

# @socketio.on('fill')
# def send_json(json):
#     socketio.emit(json, json=True)
def called():
    print('\n\n\n\n', 'received', '\n\n\n\n')





# test
@socketio.on('pushtest')
def pushtest(test, id):

    print('\n\n\n', 'id: ', id, '  test:   ', test, '\n\n\n')
    new=Test(test=test)
    db.session.add(new)
    db.session.flush()
    db.session.commit()
    new = str('<li>'+id+": "+test+'</li>')
    emit('filltest', new)