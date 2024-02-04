import copy


class Game:
    def __init__(self):
        self.board_size = 9
        self.starting_board = [[' ' for i in range(self.board_size)] for j in range(self.board_size)]
        self.current_board = copy.deepcopy(self.starting_board)
        self.boards = [copy.deepcopy(self.current_board)]
        self.players = []
        self.winner = ''
        self.pass_count = 0
        self.self_capture = False
        self.komi_on = False
        self.komi = 0
        self.player_1_turn = True
        self.recap_on = True


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


row_alpha_dict = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8}
row_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
board = [[' ' for i in range(9)] for j in range(9)]
exit_game = False


def play_game():
    global game
    game = Game()
    global exit_game
    print("Welcome to Weiqi")
    print("enter 'exit' to quit at any time")
    choose_settings(game)
    # game.boards.append(copy.deepcopy(board))
    while not exit_game and game.pass_count < 2:
        next_turn(game)
    decide_winner(game)
    recap(game)


def print_board(board_input):
    global row_letters
    print('  [ 1    2    3    4    5    6    7    8    9 ]')
    for i, row in enumerate(board_input):
        print(row_letters[i] + ' ' + str([str(row[j]) for j in range(len(row))]))


def take_move_input(current_player):
    global game
    global board
    global exit_game
    valid_move = False
    while not exit_game and not valid_move:
        move_input = input('Enter Move: ')
        if move_input.lower() == "exit":
            exit_game = True
            break
        if move_input.lower() == "resign":
            resign(current_player)
            exit_game = True
            break
        if move_input.lower() == "pass":
            game.player_1_turn = not game.player_1_turn
            game.pass_count += 1
            if game.pass_count > 1:
                print("Both players pass")
            break
        valid_move = validate_move(move_input)
        if valid_move:
            move_row = move_input[0].upper()
            move_col = int(move_input[1]) - 1
            if game.player_1_turn:
                piece = Piece('B', (row_alpha_dict.get(move_row), move_col))
            else:
                piece = Piece('W', (row_alpha_dict.get(move_row), move_col))
            board[row_alpha_dict.get(move_row)][move_col] = piece
            check_liberties(board)
            game.player_1_turn = not game.player_1_turn
            # print("Valid move") # for testing
            game.boards.append(copy.deepcopy(board))
        else:
            print("Invalid move")


def validate_move(move_input):
    if len(move_input) != 2:
        return False
    if not move_input[1].isnumeric() or int(move_input[1]) not in range(0, 10):
        print('Invalid Column')
        return False
    if not move_input[0].isalpha or move_input[0].upper() not in row_alpha_dict:
        print('Invalid Row')
        return False
    move_row = move_input[0].upper()
    move_col = int(move_input[1])
    # print(move_row, move_col) # for testing
    if board[row_alpha_dict.get(move_row)][move_col - 1] != ' ':
        print('Space already taken')
        return False
    return True


def resign(current_player):
    print(current_player.name + " has resigned")
    current_player.resigned = True


def check_liberties(board_input):
    global game
    for i in range(len(board_input)):
        for j in range(len(board_input[0])):
            if type(board[i][j]) is Piece:
                piece = board[i][j]
                color = piece.color
                coordinates = piece.coordinates
                row = coordinates[0]
                col = coordinates[1]
                # print("Coordinates: " + str(coordinates)) # for testing
                piece.liberties = 4
                if row == 0 or row == 8:
                    piece.liberties -= 1
                if col == 0 or col == 8:
                    board[i][j].liberties -= 1
                if i > 0 and type(board[i - 1][j]) is Piece and board[i - 1][j].color != color:
                    board[i][j].liberties -= 1
                if i < 8 and type(board[i + 1][j]) is Piece and board[i + 1][j].color != color:
                    board[i][j].liberties -= 1
                if j > 0 and type(board[i][j - 1]) is Piece and board[i][j - 1].color != color:
                    board[i][j].liberties -= 1
                if j < 8 and type(board[i][j + 1]) is Piece and board[i][j + 1].color != color:
                    board[i][j].liberties -= 1
                if board[i][j].liberties < 1:
                    if board[i][j].color == "B":
                        game.players[1].score += 1
                    if board[i][j].color == "W":
                        game.players[0].score += 1
                    board[i][j] = ' '
    # print_liberties(board_input) # for testing


def decide_winner(game):
    player1 = game.players[0]
    player2 = game.players[1]
    if player1.score > player2.score and not player1.resigned:
        game.winner = player1
    elif player2.resigned:
        game.winner = player1
    else:
        game.winner = player2
    check_score(board)
    print("Scores")
    print("Player 1: " + str(player1.score))
    print("Player 2: " + str(player2.score))
    print(game.winner.name + " won")


def check_score(board_input):
    global game
    for i in range(len(board_input)):
        for j in range(len(board_input[0])):
            if type(board[i][j]) is Piece:
                piece = board[i][j]
                color = piece.color
                if color == "B":
                    game.players[0].score += 1
                if color == "W":
                    game.players[1].score += 1


def recap(game):
    if game.recap_on:
        for old_board in game.boards:
            print_board(old_board)
    # recap_input = input("Show game recap?: ").lower()
    # if recap_input[0].lower() == "y":
    #     for old_board in game.boards:
    #         print_board(old_board)


def choose_settings(game):
    player1 = Player('player 1')
    player2 = Player('player 2')
    game.players = [player1, player2]
    komi_input = input("Enter komi ")
    if komi_input[0] == "0":
        game.komi_on = False
    else:
        game.komi = float(komi_input)
        player2.score += game.komi


def next_turn(game):
    current_player = game.players[not game.player_1_turn]
    print(current_player.name + "'s turn")
    print_board(board)
    take_move_input(current_player)


def print_liberties(board_input):
    for i, row in enumerate(board_input):
        print(row_letters[i] + ' ' + str([str(row[j].liberties) if type(row[j]) is Piece else str(row[j]) for j in range(0, 9)]))


if __name__ == '__main__':
    play_game()
