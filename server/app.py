from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit, join_room
from main import Game, Player
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")
CORS(app)
games = dict()
players = dict()


@app.route("/create_game", methods=["POST"])
def create_game():

    data = request.json
    player_creator = int(data['player_creator'])
    game = Game(player_creator)
    games[game.game_id] = game
    return jsonify(dict(game_id=game.game_id))


@socketio.on("echo")
def echo(ws):
    print('received message: ' + ws)
    emit(ws, json=True)


@socketio.on("Хуй соси")
def echo(ws):
    print('received message: ' + ws)
    emit(ws, json=True)


@socketio.on('connect_to_game')
def test_connect(data):

    game_id = int(data['game_id'])
    player_id = int(data['player_id'])

    room = game_id
    join_room(room)
    player = players[player_id]
    player.sid = request.sid
    game = games[game_id]
    game.add_player(player)
    emit("connected_to_game", json=True, to=game_id)
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
        if game.check_end_game():
            emit("end_game", (players[player_id].name), to=game_id)


@socketio.on("restart_game")
def restart_game(data):

    game_id = data.get_id
    game: Game = games[game_id]
    game.next_round()


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    name = data.get("login")
    player = Player(name)
    players[player.player_id] = player
    return jsonify(dict(player_id=player.player_id))


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
