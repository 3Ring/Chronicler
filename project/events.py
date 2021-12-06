from flask_socketio import emit

from project.__init__ import db, socketio
from project.models import BridgeGameCharacters, Sessions, Characters, Notes
from project.helpers import make_character_images, private_convert
from project.socket_helper import translate_jinja

# variables
class__buttonEdit = "note_edit_button"
imageLink__defaultCharacter = "/static/images/default_character.jpg"
imageLink__defaultGame = "/static/images/default_game.jpg"
imageLink__defaultDm = "/static/images/default_dm.jpg"
imageLink__buttonEdit = "/static/images/edit_button_image.png"

idPrefix__newSessionHeader = "session_header_"
idPrefix__newSessionCard = "session_card_"

# Create, store and return new session on new session event
@socketio.on("send_new_session")
def send_new_session(game_id, number, title, synopsis=None):
    print("here in session")
    # convert message to model and add to db
    new = Sessions.create(
        number=number, title=title, synopsis=synopsis, game_id=game_id
    )

    # convert data to html element
    elements = translate_jinja(new, "session", game_id)

    # return data to client
    emit(
        "fill_new_session",
        (elements["card"], elements["nav"], str(number)),
        broadcast=True,
    )


@socketio.on("send_new_note")
def send_new_note(
    user_id,
    game_id,
    dm_id,
    character_id,
    session_number,
    note,
    private_=False,
    to_dm=False,
):

    private2 = private_convert(private_)
    to_dm = private_convert(to_dm)
    user_char_list = Characters.query.filter_by(user_id=user_id).all()
    bridge_char_list = BridgeGameCharacters.query.filter_by(game_id=game_id).all()
    current_char_id = character_id

    current_char = Characters.get_from_id(current_char_id)
    session_number = session_number

    new = Notes.create(
        charname=current_char.name,
        session_number=session_number,
        text=note,
        private=private2,
        to_dm=to_dm,
        origin_character_id=character_id,
        user_id=user_id,
        game_id=game_id,
    )

    note_for_current_user = translate_jinja(
        new,
        "note",
        game_id,
        u_id=user_id,
        d_id=dm_id,
        c_user=user_id,
        char_img=new.char_img,
    )["no_sections"]

    note_for_dm = translate_jinja(
        new,
        "note",
        game_id,
        u_id=dm_id,
        d_id=dm_id,
        c_user=dm_id,
        char_img=new.char_img,
    )["no_sections"]

    note_for_other = translate_jinja(
        new, "note", game_id, u_id=False, d_id=False, c_user=-1, char_img=new.char_img
    )["no_sections"]

    element_list = [note_for_current_user, note_for_dm, note_for_other]

    emit(
        "fill_new_note",
        (
            element_list,
            new.text,
            new.private,
            new.to_dm,
            new.id,
            new.session_number,
            user_id,
        ),
        broadcast=True,
    )


def send_editted_note(
    note,
    text,
    user_id,
    game_id,
    dm_id,
    character_id,
    _private,
    changed,
    was_not_private,
    was_draft,
    _to_dm,
):

    char_img = Characters.get_from_id(character_id).image
    # char_img = make_character_images(current_char.id)
    note.text = text
    note.private = _private
    # note.char_img = char_img
    note.to_dm = _to_dm

    db.session.flush()
    db.session.commit()

    note_for_current_user = translate_jinja(
        note,
        "note",
        game_id,
        u_id=user_id,
        d_id=dm_id,
        c_user=user_id,
        char_img=char_img,
    )["no_sections"]

    note_for_dm = translate_jinja(
        note, "note", game_id, u_id=user_id, d_id=dm_id, c_user=dm_id, char_img=char_img
    )["no_sections"]

    note_for_other = translate_jinja(
        note, "note", game_id, u_id=dm_id, d_id=dm_id, c_user=-99, char_img=char_img
    )["no_sections"]

    editted_note_list = [note_for_current_user, note_for_dm, note_for_other]
    emit(
        "fill_note_edit",
        (
            editted_note_list,
            note.text,
            note.private,
            note.to_dm,
            note.id,
            user_id,
            changed,
            was_not_private,
            was_draft,
        ),
        broadcast=True,
    )


@socketio.on("edit_note")
def edit_note(text, is_private, to_dm, character_id, dm_id, game_id, user_id, note_id):

    _to_dm = private_convert(to_dm)
    _private = private_convert(is_private)

    note = Notes.query.filter_by(id=note_id).first()
    if note.private != _private or note.to_dm != _to_dm:
        changed = True
    else:
        changed = False
    if note.private == False and note.to_dm == False:
        was_not_private = True
    else:
        was_not_private = False
    if note.private == True:
        was_draft = True
    else:
        was_draft = False

    # these are separated to make sure that if the filler needs to be made then that is done by the client before emitting the new note.
    if (
        note.to_dm == True
        and _to_dm == False
        or note.private == True
        and _private == False
    ):
        ordered_session_note_list = (
            Notes.query.filter_by(session_number=note.session_number)
            .order_by(Notes.date_added.desc())
            .all()
        )
        _id_list = []
        list_location = 0
        for i, _list in enumerate(ordered_session_note_list):
            _id_list.append(_list.id)
            if _list.id == int(note_id):
                list_location = i

        emit(
            "make_filler",
            (
                note_id,
                _id_list,
                list_location,
                note.session_number,
                text,
                _private,
                _to_dm,
                dm_id,
                game_id,
                user_id,
                note_id,
            ),
            broadcast=True,
        )
        send_editted_note(
            note,
            text,
            user_id,
            game_id,
            dm_id,
            character_id,
            _private,
            changed,
            was_not_private,
            was_draft,
            _to_dm,
        )
    else:
        send_editted_note(
            note,
            text,
            user_id,
            game_id,
            dm_id,
            _private,
            changed,
            was_not_private,
            was_draft,
            _to_dm,
        )


@socketio.on("delete_note")
def delete_note(id_num):
    note = Notes.query.filter_by(id=id_num).first()
    db.session.delete(note)
    db.session.commit()
    emit("remove_deleted_note", id_num, broadcast=True)
