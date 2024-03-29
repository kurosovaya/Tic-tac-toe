from random import randint


class Player:

    sid = None

    def __init__(self, name: str):

        self.player_id = randint(10000, 99999)
        self.name = name


class Game:

    def __init__(self, player_creator):

        self.game_id = randint(10000, 99999)
        self.game_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player_creator = player_creator
        self.player_current_turn = player_creator
        self.player_crosses = None
        self.player_noughts = None
        self.spectators = []
        self.cross = "X"
        self.nought = "O"
        self.current_sight = self.nought
        self.messages = list()
        self.game_end = False

    def move(self, x, y, player_id):

        if self.game_board[x][y] == 0 and player_id == self.player_current_turn and not self.game_end:
            self.current_sight = self.cross if self.current_sight == self.nought else self.nought
            self.game_board[x][y] = self.current_sight
            self.player_current_turn = self.player_noughts.player_id if player_id == self.player_crosses.player_id else self.player_crosses.player_id
            return True
        else:
            return False

    def check_end_game(self):

        def check_win(check_list):
            for i in range(1, len(check_list)):
                if check_list[i-1] != check_list[i] or check_list[i-1] == 0:
                    return False
            return True

        def check_draw(board):
            if 0 in set([x for j in board for x in j]):
                return False
            else:
                return True

        check_rows = []

        for i in range(len(self.game_board)):
            check_rows.append(self.game_board[i])
            check_rows.append([self.game_board[j][i] for j in range(len(self.game_board))])

        check_rows.append([self.game_board[i][i] for i in range(3)])
        diagonal = []
        for i, j in zip(range(3), range(2, -1, -1)):
            diagonal.append(self.game_board[i][j])
        check_rows.append(diagonal)

        for row in check_rows:
            if check_win(row):
                self.game_end = True
                return True

        if check_draw(self.game_board):
            self.game_end = True
            return None

        return False

    def add_player(self, player):

        if self.player_crosses is None:
            self.player_crosses = player
        elif self.player_noughts is None and self.player_crosses.player_id != player.player_id:
            self.player_noughts = player
        else:
            self.spectators.append(Player)

    def swap_players(self, player_one="X", player_two="O"):

        self.player_one = player_one
        self.player_two = player_two

    @property
    def game_ready(self):

        return bool(self.player_crosses and self.player_noughts)

    def draw(self):

        for i in range(3):
            for j in range(3):
                print(self.game_board[i][j], end=" | ")
            print()

    def next_round(self):

        self.game_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player_crosses, self.player_noughts = self.player_noughts, self.player_crosses
        self.current_sight = self.nought
        self.game_end = False

# game = Game()

# while not game.check_end_game():
#     game.draw()
#     i, j, val = input().split(",")
#     game.move(int(i), int(j), val)
