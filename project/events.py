from .__init__ import db, socketio
from .classes import *
from flask_socketio import emit
from .helpers import validate as v
def called():
    print('\n\n\n\n', 'received', '\n\n\n\n')

@socketio.on('send_new_session')
def send_new_session(id, number, title, synopsis=None):
    new=Sessions(number=number, title=title, synopsis=synopsis, games_id=id)
    db.session.add(new)
    db.session.flush()
    db.session.commit()
    newsession = str("<div id='session"+str(new.number)+"'>Session"+str(new.number)+": "+new.title+"</div")
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
    # current_game = Games.query.filter_by(id=game_id).first()


    current_char=Characters.query.filter_by(user_id=user_id, game_id=game_id).first()[0]
    session_number=Sessions.query.with_entities(Sessions.number).filter_by(games_id=game_id).order_by(Sessions.number.desc()).first()[0]
    # this will cause issues if a player has more than one character for now

    print('\n\n\n\n', "game_id:", game_id, "user_id:", user_id, "note:", note, "Private:", private, "in_character", in_character, "charname", current_char.name, "character(id):", current_char.id, "session_number:", session_number)

    new=Notes(charname=current_char.name, note=note, session_number=session_number, private=private, in_character=in_character, character=current_char.id , user_id=user_id, game_id=game_id)
    
    db.session.add(new)
    db.session.flush()
    new_note=str("<p id='note"+str(new.id)+"'>"+str(new.charname)+":  "+str(new.note)+"</p>")
    print('\n\n\n\n', new_note)
    
    emit('fill_new_note', (new_note, new.private, new.session_number, new.in_character), broadcast=True)
    db.session.commit()

# @socketio.on('delete_note_fill')
# def delete_note(note_id, index, user_id):

#     v(note_id, 'note_id')
#     v(user_id, 'user_id')

    # item_to_delete = table.query.filter_by(id=id).first()
    # v(item_to_delete, 'item_to_delete')



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
