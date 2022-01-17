from flask_socketio import emit
from project.helpers.db_session import db_session
from project.__init__ import socketio
from project.models import Sessions, Notes



@socketio.on("check_delete_session")
def check_delete(session_id):
    """delete session if session does not contain any notes"""
    session = Sessions.query.get(session_id)
    notes = Notes.get_list_from_session_number(session.number, session.game_id)
    if notes:
        emit("check_delete_session_fail")
    else:
        with db_session():
            session.delete_self()
        emit("check_delete_session_pass", session.number)


@socketio.on("edit_session")
def edit_session(id_, new_number, new_title):
    session = Sessions.query.get(id_)
    old_title = session.title
    old_number = session.number
    if (
        Sessions.query.filter_by(id=id_).first().number != int(new_number)
        and Sessions.query.filter_by(game_id=session.game_id, number=new_number).first()
    ):
        emit("session_number_conflict")
        return
    notes = Notes.get_list_from_session_number(old_number, session.game_id)
    for note in notes:
        note.update(session_number=new_number)
    session.update(number=new_number, title=new_title)
    emit(
        "fill_edit_session",
        (old_title, new_title, str(new_number), old_number),
        broadcast=True,
    )