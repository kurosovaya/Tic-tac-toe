from flask import Flask, jsonify, request
from flask_sock import Sock
from main import Game, Player

app = Flask(__name__)
sock = Sock(app)
games = dict()
players = dict()


@app.route("/create_game", methods=["POST"])
def create_game():
    game = Game()
    games[game.game_id] = game
    return jsonify(dict(game_id=game.game_id))


@sock.route("/echo")
def echo(ws):
    while True:
        data = ws.receive()
        ws.send(data)


@app.route("/move", methods=["POST"])
def move():
    data = request.json
    game_id = data.get("game_id")
    player_id = data.get("player_id")
    x_axis = data.get("x_axis")
    y_axis = data.get("y_axis")

    game = games[int(game_id)]

    game.move(x_axis, y_axis, "x")

    return jsonify(dict(game_board=game.game_board))


@app.route("/connect_to_game")
def connect_to_game():
    data = request.json

    game_id = data.game_id
    player_id = data.player_id

    player = players[player_id]

    games[game_id].add_player(player)
    # TODO response


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    name = data.get("login")
    player = Player(name)
    players[player.player_id] = player
    return jsonify(dict(player_id=player.player_id))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
