import copy


class Game:
    def __init__(self):
        self.boards = []
        self.winner = ''


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0


class Piece:
    def __init__(self, color):
        self.color = color
        self.liberties = 4

    def __str__(self):
        return self.color


player1 = Player('')
player2 = Player('')
game = None

row_alpha_dict = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8}
row_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
board = [[' ' for i in range(0, 9)] for j in range(0, 9)]
exit_game = False
player_1_turn = True
players = [player1, player2]


def play_game():
    global game
    game = Game()
    global exit_game
    print("Welcome to Weiqi")
    print("enter 'exit' to quit at any time")
    komi_on = input("Play with Komi? ")
    if komi_on[0].lower() == "y":
        player2.score += 6.5
    player1.name = 'player 1'
    player2.name = 'player 2'
    game.boards.append(copy.deepcopy(board))
    while not exit_game:
        current_player = players[not player_1_turn].name
        print(current_player + "'s turn")
        print_board(board)
        take_move_input(current_player)
    if player1.score > player2.score:
        game.winner = player1
    else:
        game.winner = player2
    print(player1.score)
    print(player2.score)
    print(game.winner.name + " won")
    recap = input("Show game recap?: ").lower()
    if recap[0].lower() == "y":
        for old_board in game.boards:
            print_board(old_board)


def print_board(board_input):
    global row_letters
    print('  [ 1    2    3    4    5    6    7    8    9 ]')
    for i, row in enumerate(board_input):
        print(row_letters[i] + ' ' + str([str(row[j]) for j in range(len(row))]))


def take_move_input(current_player):
    global game
    global board
    global exit_game
    global player_1_turn
    valid_move = False
    while not exit_game and not valid_move:
        move_input = input('Enter Move: ')
        if move_input == "exit":
            exit_game = True
            break
        if move_input == "resign":
            resign(current_player)
            exit_game = True
            break
        move_row = move_input[0].upper()
        move_col = int(move_input[1])
        valid_move = validate_move(move_row, move_col)
        if valid_move:
            if player_1_turn:
                piece = Piece('B')
            else:
                piece = Piece('W')
            board[row_alpha_dict.get(move_row)][move_col - 1] = piece
            check_liberties(board)
            player_1_turn = not player_1_turn
            print("Valid move")
            game.boards.append(copy.deepcopy(board))
        else:
            print("Invalid move")


def validate_move(move_row, move_col):
    print(move_row, move_col)
    if move_row not in row_alpha_dict:
        print('Invalid Row')
        return False
    if move_col not in range(0, 10):
        print('Invalid Column')
        return False
    if board[row_alpha_dict.get(move_row)][move_col - 1] != ' ':
        print('Space already taken')
        return False
    return True


def resign(current_player):
    print(current_player + " has resigned")


def check_liberties(board_input):
    for i in range(len(board_input)):
        for j in range(len(board_input[0])):
            if type(board[i][j]) is Piece:
                board[i][j].liberties = 4
                if i == 0 or i == 8:
                    board[i][j].liberties -= 1
                if j == 0 or j == 8:
                    board[i][j].liberties -= 1
                if board[i - 1][j] and type(board[i - 1][j]) is Piece and board[i - 1][j].color != board[i][j].color:
                    board[i][j].liberties -= 1
                if board[i + 1][j] and type(board[i + 1][j]) is Piece and board[i + 1][j].color != board[i][j].color:
                    board[i][j].liberties -= 1
                if board[i][j - 1] and type(board[i][j - 1]) is Piece and board[i][j - 1].color != board[i][j].color:
                    board[i][j].liberties -= 1
                if board[i][j + 1] and type(board[i][j + 1]) is Piece and board[i][j + 1].color != board[i][j].color:
                    board[i][j].liberties -= 1
                if board[i][j].liberties < 1:
                    board[i][j] = ' '

    for i, row in enumerate(board_input):
        print(row_letters[i] + ' ' + str([str(row[j].liberties) if type(row[j]) is Piece else str(row[j]) for j in range(0, 9)]))


if __name__ == '__main__':
    play_game()