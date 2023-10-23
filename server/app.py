from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit, join_room
from main import Game, Player
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
games = dict()
players = dict()


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    name = data.get("login")
    player = Player(name)
    players[player.player_id] = player
    return jsonify(dict(player_id=player.player_id))


@app.route("/create_game", methods=["POST"])
def create_game():

    data = request.json
    player_creator = int(data['player_creator'])
    game = Game(player_creator)
    games[game.game_id] = game
    return jsonify(dict(game_id=game.game_id))


@socketio.on('connect_to_game')
def connect_to_game(data):

    game_id = int(data['game_id'])
    player_id = int(data['player_id'])

    room = game_id
    join_room(room)
    player = players[player_id]
    player.sid = request.sid
    game = games[game_id]
    game.add_player(player)
    emit("send_system_message", f"Player {players[player_id].name} connected to game", to=game_id)
    if game.game_ready:
        emit("game_ready", to=game_id)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on("check_move")
def move(data):
    game_id = int(data.get("game_id"))
    player_id = data.get("player_id")
    x_axis = data.get("x_axis")
    y_axis = data.get("y_axis")
    game: Game = games[game_id]
    if game.move(x_axis, y_axis, player_id):
        emit("make_move", (x_axis, y_axis, game.current_sight), to=game_id)
        game_status = game.check_end_game()
        if game_status:
            emit("end_game", (players[player_id].name), to=game_id)
        elif game_status is None:
            emit("draw", to=game_id)


@socketio.on("restart_game")
def restart_game(data):

    game_id = int(data.get("game_id"))
    game: Game = games[game_id]
    game.next_round()
    emit("restart_game", to=game_id)


@socketio.on("get_field")
def get_field(data):
    game_id = int(data.get("game_id"))
    game: Game = games[game_id]
    return game.game_board


@socketio.on("get_chat_history")
def get_chat_history(data):
    game_id = int(data.get("game_id"))
    game: Game = games[game_id]
    return game.messages


@socketio.on("send_message")
def send_message(data):
    game_id = int(data.get("game_id"))
    message = data.get("message")
    time = data.get("time")
    player_id = data.get("player_id")
    message_type = data.get("message_type")
    player_name = players[player_id].name
    game: Game = games[game_id]
    game.messages.append({"player_name": player_name,
                          "message": message,
                          "time": time,
                          "message_type": message_type})
    emit("get_message", {"player_name": player_name,
                         "message": message,
                         "time": time,
                         "message_type": message_type}, to=game_id)


@socketio.on("send_system_message")
def send_system_message(data):
    game_id = int(data.get("game_id"))
    message = data.get("message")
    time = data.get("time")
    message_type = data.get("message_type")
    game: Game = games[game_id]
    game.messages.append({"message": message,
                          "time": time,
                          "message_type": message_type})
    emit("get_message", {"message": message,
                         "time": time,
                         "message_type": message_type}, to=game_id)


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, host='0.0.0.0', port=5000)
