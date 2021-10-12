from .__init__ import db, socketio
from .classes import *
from flask_socketio import emit
from .helpers import make_character_images, priv_convert
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
def send_new_note(user_id, game_id, dm_id, session_number, note, priv=False, to_gm=False):

    private2 = priv_convert(priv)
    to_gm = priv_convert(to_gm)
    
    current_char=Characters.query.filter_by(user_id=user_id, game_id=game_id).first()
    char_img = make_character_images(current_char.id)
    session_number=session_number

    # this will cause issues if a player has more than one character for now
    new=Notes(charname=current_char.name, session_number=session_number, note=note, private=private2, to_gm=to_gm, character=current_char.id , user_id=user_id, game_id=game_id)
    new.char_img = char_img
    db.session.add(new)
    db.session.flush()
    db.session.commit()

    note_for_current_user = translate_jinja(new, "note", game_id, u_id=user_id, d_id=dm_id, c_user=user_id, char_img=char_img)["no_sections"]

    note_for_dm = translate_jinja(new, "note", game_id, u_id=dm_id, d_id=dm_id, c_user=dm_id, char_img=char_img)["no_sections"]

    note_for_other = translate_jinja(new, "note", game_id, u_id=False, d_id=False, c_user=-1, char_img=char_img)["no_sections"]
 
    element_list = [ 
        note_for_current_user
        , note_for_dm
        , note_for_other
    ]

    emit('fill_new_note', (element_list, new.note, new.private, new.to_gm, new.id, new.session_number, user_id), broadcast=True)
    
def send_editted_note(note, text, user_id, game_id, dm_id, _private, changed, was_not_private, was_draft, _to_dm):

    current_char=Characters.query.filter_by(user_id=user_id, game_id=game_id).first()
    char_img = make_character_images(current_char.id)
    note.note = text
    note.private = _private
    note.char_img = char_img
    note.to_gm = _to_dm

    db.session.flush()
    db.session.commit()

    note_for_current_user = translate_jinja(note, "note", game_id, u_id=user_id, d_id=dm_id, c_user=user_id, char_img=char_img)["no_sections"]

    note_for_dm = translate_jinja(note, "note", game_id, u_id=user_id, d_id=dm_id, c_user=dm_id, char_img=char_img)["no_sections"]

    note_for_other = translate_jinja(note, "note", game_id, u_id=dm_id, d_id=dm_id, c_user=-1, char_img=char_img)["no_sections"]
 
    editted_note_list = [ 
        note_for_current_user
        , note_for_dm
        , note_for_other
    ]
    emit('fill_note_edit', (editted_note_list, note.note, note.private, note.to_gm, note.id, user_id, changed, was_not_private, was_draft), broadcast=True)

@socketio.on('edit_note')
def edit_note(text, is_private, to_dm, dm_id, game_id, user_id, note_id):

    _to_dm = priv_convert(to_dm)
    _private = priv_convert(is_private)

    note = Notes.query.filter_by(id=note_id).first()
    if note.private != _private or note.to_gm != _to_dm:
        changed = True
    else:
        changed = False
    if note.private == False and note.to_gm == False:
        was_not_private = True
    else:
        was_not_private = False
    if note.private == True:
        was_draft = True
    else:
        was_draft = False

    # these are separated to make sure that if the filler needs to be made then that is done by the client before emitting the new note.
    if note.to_gm == True and _to_dm == False or note.private == True and _private == False:
        ordered_session_note_list = Notes.query.filter_by(session_number = note.session_number).order_by(Notes.date_added.desc()).all()
        _id_list = []
        list_location = 0
        for i, _list in enumerate(ordered_session_note_list):
            _id_list.append(_list.id)
            if _list.id == int(note_id):
                list_location = i

        emit("make_filler", (note_id, _id_list, list_location, note.session_number, text, _private, _to_dm, dm_id, game_id, user_id, note_id), broadcast=True)
        send_editted_note(note, text, user_id, game_id, dm_id, _private, changed, was_not_private, was_draft, _to_dm)
    else:
        send_editted_note(note, text, user_id, game_id, dm_id, _private, changed, was_not_private, was_draft, _to_dm)


    
    
@socketio.on("delete_note")
def delete_note(id_num):
    note = Notes.query.filter_by(id=id_num).first()
    db.session.delete(note)
    db.session.commit()
    emit('remove_deleted_note', id_num, broadcast=True)
 
    

