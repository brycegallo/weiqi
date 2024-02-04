import copy


class Game:
    def __init__(self):
        self.board_size = 9
        self.starting_board = [[' ' for i in range(self.board_size)] for j in range(self.board_size)]
        self.current_board = copy.deepcopy(self.starting_board)
        self.boards = [copy.deepcopy(self.current_board)]
        self.players = [Player('Player 1'), Player('Player 2')]
        self.winner = ''
        self.pass_count = 0
        self.self_capture = False
        self.komi_on = True # can be True for testing, should default to False
        self.komi = 0
        self.turn = 0
        self.current_player = self.players[0]
        self.waiting_player = self.players[1]
        self.recap_on = False # can be True for testing, should default to False
        self.end_game = False
        self.row_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        self.row_alpha_dict = dict((letter, i) for i, letter in enumerate(self.row_letters))


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.resigned = False


class Piece:
    def __init__(self, color, coordinates):
        self.color = color
        self.liberties = 4
        self.coordinates = coordinates

    def __str__(self):
        return self.color


class Group:
    def __init__(self):
        self.pieces = []
        self.liberties = 4


class Board:
    def __init__(self, size):
        self.size = size
        self.positions = []
        self.row_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        self.row_alpha_dict = dict((letter, i) for i, letter in enumerate(self.row_letters))


def play_game():
    game = Game()
    print("Welcome to Weiqi")
    print("enter 'exit' to quit at any time")
    choose_settings(game)
    while not game.end_game and game.pass_count < 2:
        next_turn(game)
    decide_winner(game)
    recap(game)


def print_board(game):
    board = game.current_board
    row_letters = game.row_letters
    print('  [ 1    2    3    4    5    6    7    8    9 ]')
    for i, row in enumerate(board):
        print(row_letters[i] + ' ' + str([str(row[j]) for j in range(len(row))]))


def take_move_input(game):
    valid_move = False
    while not game.end_game and not valid_move:
        move_input = input('Enter Move: ')
        if move_input.lower() == "exit" or move_input.lower() == "resign":
            if move_input.lower() == "resign":
                resign(game)
            game.end_game = True
            break
        if move_input.lower() == "pass":
            game.pass_count += 1
            if game.pass_count > 1:
                print("Both players pass")
            break
        valid_move = validate_move(game, move_input)
        if valid_move:
            ra_dict = game.row_alpha_dict
            game.pass_count = 0
            move_row = move_input[0].upper()
            move_col = int(move_input[1]) - 1
            if game.current_player == game.players[0]:
                piece = Piece('B', (ra_dict.get(move_row), move_col))
            else:
                piece = Piece('W', (ra_dict.get(move_row), move_col))
            game.current_board[ra_dict.get(move_row)][move_col] = piece
            check_game_liberties(game)
            # print("Valid move") # for testing
            game.boards.append(copy.deepcopy(game.current_board))
        else:
            print("Invalid move")


def validate_move(game, move_input):
    ra_dict = game.row_alpha_dict
    if len(move_input) != 2:
        return False
    if not move_input[1].isnumeric() or int(move_input[1]) not in range(0, 10):
        print('Invalid Column')
        return False
    if not move_input[0].isalpha or move_input[0].upper() not in ra_dict:
        print('Invalid Row')
        return False
    move_row = move_input[0].upper()
    move_col = int(move_input[1])
    # print(move_row, move_col) # for testing
    if game.current_board[ra_dict.get(move_row)][move_col - 1] != ' ':
        print('Space already taken')
        return False
    return True


def resign(game):
    if game.current_player == game.players[0]:
        game.players[0].resigned = True
        print(game.players[0].name + " has resigned")
    else:
        game.players[1].resigned = True
        print(game.players[1].name + " has resigned")


def check_game_liberties(game):
    board = game.current_board
    for i in range(len(board)):
        for j in range(len(board[0])):
            position = board[i][j]
            if type(position) is Piece:
                piece = position
                color = piece.color
                coordinates = piece.coordinates
                row = coordinates[0]
                col = coordinates[1]
                # print("Coordinates: " + str(coordinates)) # for testing
                piece.liberties = 4
                if row == 0 or row == 8:
                    piece.liberties -= 1
                if col == 0 or col == 8:
                    piece.liberties -= 1
                if i > 0 and type(board[i - 1][j]) is Piece and board[i - 1][j].color != color:
                    piece.liberties -= 1
                if i < 8 and type(board[i + 1][j]) is Piece and board[i + 1][j].color != color:
                    piece.liberties -= 1
                if j > 0 and type(board[i][j - 1]) is Piece and board[i][j - 1].color != color:
                    piece.liberties -= 1
                if j < 8 and type(board[i][j + 1]) is Piece and board[i][j + 1].color != color:
                    piece.liberties -= 1
                if piece.liberties < 1:
                    if piece.color == "B":
                        game.players[1].score += 1
                    if piece.color == "W":
                        game.players[0].score += 1
                    board[i][j] = ' '
    # print_liberties(game)  # for testing


def check_group_liberties(game):
    pass


def decide_winner(game):
    player1 = game.players[0]
    player2 = game.players[1]
    if player1.score > player2.score and not player1.resigned:
        game.winner = player1
    elif player2.resigned:
        game.winner = player1
    else:
        game.winner = player2
    check_game_score(game)
    print("Scores")
    print("Player 1: " + str(player1.score))
    print("Player 2: " + str(player2.score))
    print(game.winner.name + " won")


def check_game_score(game):
    board = game.current_board
    for i in range(len(board)):
        for j in range(len(board[0])):
            if type(board[i][j]) is Piece:
                piece = board[i][j]
                color = piece.color
                if color == "B":
                    game.players[0].score += 1
                if color == "W":
                    game.players[1].score += 1


def recap(game):
    # recap_input = input("Show game recap?: ").lower()
    # if recap_input[0].lower() == "y":
    #     game.recap_on = True
    if game.recap_on:
        for old_board in game.boards:
            print_board(old_board)


def choose_settings(game):
    # game.current_player.name = input("Player 1 enter name")
    # game.waiting_player.name = input("Player 2 enter name")
    # uncomment above after testing

    # komi_input = input("Enter komi ")
    # if komi_input[0] == "0":
    #     game.komi_on = False
    # else:
    #     game.komi = float(komi_input)
    #     player2.score += game.komi
    game.komi = 6.5 # for testing, remove and uncomment above, later
    game.players[1].score += game.komi


def next_turn(game):
    if game.turn > 0:
        swap_players(game)
    game.turn += 1
    print(game.current_player.name + "'s turn")
    print_board(game)
    take_move_input(game)


def swap_players(game):
    game.current_player, game.waiting_player = game.waiting_player, game.current_player


def print_liberties(game):
    board = game.current_board
    letters = game.row_letters
    for i, row in enumerate(board):
        print(letters[i] + ' ' + str([str(row[j].liberties) if type(row[j]) is Piece else str(row[j]) for j in range(9)]))


# Board Analysis-Specific Functions
# def print_liberties(board_input):
#     for i, row in enumerate(board_input):
#         print(row_letters[i] + ' ' + str([str(row[j].liberties) if type(row[j]) is Piece else str(row[j]) for j in range(9)]))

# def print_board(board_input):
#     global row_letters
#     print('  [ 1    2    3    4    5    6    7    8    9 ]')
#     for i, row in enumerate(board_input):
#         print(row_letters[i] + ' ' + str([str(row[j]) for j in range(len(row))]))

# def check_score(board_input):
#     global game
#     for i in range(len(board_input)):
#         for j in range(len(board_input[0])):
#             if type(game.current_board[i][j]) is Piece:
#                 piece = game.current_board[i][j]
#                 color = piece.color
#                 if color == "B":
#                     game.players[0].score += 1
#                 if color == "W":
#                     game.players[1].score += 1

# def print_liberties(board_input):
#     for i, row in enumerate(board_input):
#         print(row_letters[i] + ' ' + str([str(row[j].liberties) if type(row[j]) is Piece else str(row[j]) for j in range(9)]))

if __name__ == '__main__':
    play_game()
