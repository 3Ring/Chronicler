from flask_socketio import emit
from project.__init__ import socketio
from project.models import BridgeGameCharacters, Users


# @socketio.on("remove_player")
# def remove_player(user_id: int, game_id: int):
#     player = Users.get_from_id(user_id)
#     socketio.emit("remove_player_start_success", ())


@socketio.on("remove_player_final")
def remove_player(user_id: int, game_id: int):
    player = Users.get_from_id(user_id)
    bridge = BridgeGameCharacters.query.filter_by(game_id=game_id, character_id=player.id).first()
    bridge.remove_self()
    socketio.emit("remove_player_final_success") 

@socketio.on("remove_character_start")
def remove_character(user_id, game_id, character_id):
    player = Users.query.get(user_id)
    if player.get_character_list_from_game(game_id) > 1:
        socketio.emit("remove_character_start_success")
    else:
        emit("remove_player_fail")
