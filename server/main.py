from random import randint


class Player:

    sid = None

    def __init__(self, name: str):

        self.player_id = randint(10000, 99999)
        self.name = name


class Game:

    def __init__(self):

        self.game_id = randint(10000, 99999)
        self.game_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player_one = None
        self.player_two = None

    def move(self, x, y, val):

        self.game_board[x][y] = val

    def check_end_game(self):

        def check_win(check_list):
            for i in range(1, len(check_list)):
                if check_list[i-1] != check_list[i] or check_list[i-1] == 0:
                    return False
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
                return True
        return False

    def add_player(self, player):

        if self.player_one is None:
            self.player_one = player
        elif self.player_two is None:
            self.player_two = player
        else:
            return False
        return True

    @property
    def game_ready(self):

        return bool(self.player_one and self.player_two)

    def draw(self):

        for i in range(3):
            for j in range(3):
                print(self.game_board[i][j], end=" | ")
            print()


# game = Game()

# while not game.check_end_game():
#     game.draw()
#     i, j, val = input().split(",")
#     game.move(int(i), int(j), val)
