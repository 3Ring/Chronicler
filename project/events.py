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
