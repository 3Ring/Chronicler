from flask_socketio import emit

from project.extensions.socketio import socketio
from project.models import Sessions
from project.helpers.translate_jinja.translate_jinja import TranslateJinja
from project.helpers.db_session import db_session

@socketio.on("send_new_session")
def send_new_session(game_id, number, title, synopsis=None):
    with db_session():
        new = Sessions.create(
            number=number, title=title, synopsis=synopsis, game_id=game_id
        )
        elements = TranslateJinja(new, "session", game_id).run()
        emit(
            "fill_new_session",
            (elements["session_card"], elements["session_nav"], str(number)),
            broadcast=True,
        )