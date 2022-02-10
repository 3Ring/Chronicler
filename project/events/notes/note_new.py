from flask_socketio import emit
from flask_login import current_user
from project.__init__ import db, socketio
from project.models import Sessions, Characters, Notes, Users
from project.helpers.misc import private_convert
from project.helpers.translate_jinja.translate_jinja import TranslateJinja
from project.helpers.db_session import db_session


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
    with db_session():
        # !bug page code
        if character_id == "bugs":
            character_id = Users.get_avatar(current_user.id).id
        # !end bug page code
        private2 = private_convert(private_)
        to_dm = private_convert(to_dm)
        current_char_id = character_id
        current_char = Characters.query.get(current_char_id)

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
        new.attach_char_img(new)
        sockets = TranslateJinja(            
            new,
            "note",
            game_id,
            user_id=user_id,
            dm_id=dm_id,
            target_users={"user": user_id, "dm": dm_id, "other": -10},
            ).run()
        print(f'user_id: {user_id}')
        # print(f' sockets["user"]: { sockets["user"]}')
        emit(
            "fill_new_note",
            (
                [
                    sockets["user"]["no_sections"],
                    sockets["dm"]["no_sections"],
                    sockets["other"]["no_sections"],
                ],
                new.text,
                new.private,
                new.to_dm,
                new.id,
                new.session_number,
                user_id,
            ),
            broadcast=True,
        )