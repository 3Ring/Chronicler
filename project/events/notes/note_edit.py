from flask_socketio import emit
from flask_login import current_user
from project.extensions.sql_alchemy import db
from project.extensions.socketio import socketio
from project.models import Characters, Notes, Users
from project.helpers.misc import bool_convert
from project.helpers.translate_jinja.translate_jinja import TranslateJinja
from project.helpers.db_session import db_session


@socketio.on("edit_note")
def edit_note(text, is_private, to_dm, character_id, dm_id, game_id, user_id, note_id):
    # !bugs page code
    if character_id == "bugs":
        character_id = Users.get_avatar(current_user.id).id
    # !end bugs page code
    _to_dm = bool_convert(to_dm)
    _private = bool_convert(is_private)

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
    # else:
    #     send_editted_note(
    #         note,
    #         text,
    #         user_id,
    #         game_id,
    #         dm_id,
    #         character_id,
    #         _private,
    #         changed,
    #         was_not_private,
    #         was_draft,
    #         _to_dm,
    #     )


@socketio.on("delete_note")
def delete_note(id_num):
    with db_session():
        note = Notes.query.filter_by(id=id_num).first()
        db.session.delete(note)
    emit("remove_deleted_note", id_num, broadcast=True)

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
    with db_session():
        note.text = text
        note.private = _private
        note.to_dm = _to_dm
        sockets = TranslateJinja(
            note,
            "note",
            game_id,
            user_id=user_id,
            dm_id=dm_id,
            target_users={"user": user_id, "dm": dm_id, "other": -10},
        ).run()
        emit(
            "fill_note_edit",
            (
                [
                    sockets["user"]["no_sections"],
                    sockets["dm"]["no_sections"],
                    sockets["other"]["no_sections"],
                ],
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

