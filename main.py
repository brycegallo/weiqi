import collections
import copy
import re


class GameEngine:
    def __init__(self):
        self.game = self.Game()

    class Game:
        def __init__(self):
            self.settings = GameEngine.Settings()
            self.game_board = GameEngine.Board(self.settings.board_size)
            self.board_size = 9
            self.starting_board = [[' ' for i in range(self.settings.board_size)] for j in range(self.settings.board_size)]
            self.current_board = copy.deepcopy(self.starting_board)
            self.boards = [copy.deepcopy(self.current_board)]
            self.players = [GameEngine.Player('Player 1'), GameEngine.Player('Player 2')]
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
            self.eyes = 0

    class Board:
        def __init__(self, size=9):
            self.size = size
            self.initial_state = [[' ' for i in range(self.size)] for j in range(self.size)]
            self.current_state = copy.deepcopy(self.initial_state)
            self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
            self.row_letters = self.letters[:self.size]
            self.row_alpha_dict = dict((letter, i) for i, letter in enumerate(self.row_letters))

    class Settings:
        def __init__(self):
            self.board_size = 9
            self.self_capture = False
            self.komi_on = True  # can be True for testing, should default to False
            self.recap_on = False  # can be True for testing, should default to False

    def play_game(self):
        print("Welcome to Weiqi")
        print("enter 'exit' to quit at any time")
        self.choose_settings()
        while not self.game.end_game and self.game.pass_count < 2:
            self.next_turn()
        self.decide_winner()
        self.recap()

    def recap(self):
        # recap_input = input("Show game recap?: ").lower()
        # if recap_input[0].lower() == "y":
        #     game.recap_on = True
        if self.game.recap_on:
            for old_board in self.game.boards:
                self.print_board()

    def resign(self):
        if self.game.current_player == self.game.players[0]:
            self.game.players[0].resigned = True
            print(self.game.players[0].name + " has resigned")
        else:
            self.game.players[1].resigned = True
            print(self.game.players[1].name + " has resigned")

    def next_turn(self):
        if self.game.turn > 0:
            self.swap_players()
        self.game.turn += 1
        print(self.game.current_player.name + "'s turn")
        self.print_board()
        self.take_move_input()

    def swap_players(self):
        self.game.current_player, self.game.waiting_player = self.game.waiting_player, self.game.current_player

    def print_board(self):
        board = self.game.current_board
        row_letters = self.game.row_letters
        # print(
        #     re.sub("]", " ",
        #            re.sub("'", " ", str('  ' +
        #                                 re.sub(",", " ",
        #                                        str([str(i) for i in range(1, self.game.board_size)]))))) + '  ' +
        #     str(self.game.board_size) + ' ]')
        print('  [ 1    2    3    4    5    6    7    8    9 ]')
        for i, row in enumerate(board):
            print(row_letters[i] + ' ' + str([str(row[j]) for j in range(len(row))]))

    def print_liberties(self):
        board = self.game.current_board
        letters = self.game.row_letters
        for i, row in enumerate(board):
            print(letters[i] + ' ' + str([str(row[j].liberties) if type(row[j]) is GameEngine.Piece else str(row[j]) for j in range(9)]))

    def take_move_input(self):
        valid_move = False
        while not self.game.end_game and not valid_move:
            move_input = input('Enter Move: ')
            if move_input.lower() == "exit" or move_input.lower() == "resign":
                if move_input.lower() == "resign":
                    self.resign()
                self.game.end_game = True
                break
            if move_input.lower() == "pass":
                self.game.pass_count += 1
                if self.game.pass_count > 1:
                    print("Both players pass")
                break
            valid_move = self.validate_move(move_input)
            if valid_move:
                ra_dict = self.game.row_alpha_dict
                self.game.pass_count = 0
                move_row = move_input[0].upper()
                move_col = int(move_input[1]) - 1
                if self.game.current_player == self.game.players[0]:
                    piece = self.Piece('B', (ra_dict.get(move_row), move_col))
                else:
                    piece = self.Piece('W', (ra_dict.get(move_row), move_col))
                self.game.current_board[ra_dict.get(move_row)][move_col] = piece
                self.check_game_liberties()
                # print("Valid move") # for testing
                self.game.boards.append(copy.deepcopy(self.game.current_board))
            else:
                print("Invalid move")

    def validate_move(self, move_input):
        ra_dict = self.game.row_alpha_dict
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
        if self.game.current_board[ra_dict.get(move_row)][move_col - 1] != ' ':
            print('Space already taken')
            return False
        return True

    def check_game_liberties(self):
        board = self.game.current_board
        for i in range(len(board)):
            for j in range(len(board[0])):
                position = board[i][j]
                if type(position) is self.Piece:
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
                    if i > 0 and type(board[i - 1][j]) is GameEngine.Piece and board[i - 1][j].color != color:
                        piece.liberties -= 1
                    if i < 8 and type(board[i + 1][j]) is GameEngine.Piece and board[i + 1][j].color != color:
                        piece.liberties -= 1
                    if j > 0 and type(board[i][j - 1]) is GameEngine.Piece and board[i][j - 1].color != color:
                        piece.liberties -= 1
                    if j < 8 and type(board[i][j + 1]) is GameEngine.Piece and board[i][j + 1].color != color:
                        piece.liberties -= 1
                    if piece.liberties < 1:
                        if piece.color == "B":
                            self.game.players[1].score += 1
                        if piece.color == "W":
                            self.game.players[0].score += 1
                        board[i][j] = ' '
        self.print_liberties()  # for testing

    def count_groups(self):
        board = self.game.current_board
        rows = len(board)
        cols = len(board[0])
        groups = 0
        groups_surrounded = 0
        groups_w_liberties = 0
        visited = set()

        def breadth_first_search(r, c):
            dqueue = collections.deque()
            visited.add((r, c))
            dqueue.append((r, c))
            return groups

        for row in range(rows):
            for column in range(cols):
                if board[row][column] == 'B' and (row, column) not in visited:
                    breadth_first_search(row, column)
                    groups += 1

    def remove_group(self):
        for piece in self.group:
            pass

    def decide_winner(self):
        player1 = self.game.players[0]
        player2 = self.game.players[1]
        if player1.score > player2.score and not player1.resigned:
            self.game.winner = player1
        elif player2.resigned:
            self.game.winner = player1
        else:
            self.game.winner = player2
        self.check_game_score()
        print("Scores")
        print("Player 1: " + str(player1.score))
        print("Player 2: " + str(player2.score))
        print(self.game.winner.name + " won")

    def check_game_score(self):
        board = self.game.current_board
        for i in range(len(board)):
            for j in range(len(board[0])):
                if type(board[i][j]) is GameEngine.Piece:
                    piece = board[i][j]
                    color = piece.color
                    if color == "B":
                        self.game.players[0].score += 1
                    if color == "W":
                        self.game.players[1].score += 1

    def choose_settings(self):
        # game.current_player.name = input("Player 1 enter name")
        # game.waiting_player.name = input("Player 2 enter name")
        # uncomment above after testing

        # komi_input = input("Enter komi ")
        # if komi_input[0] == "0":
        #     game.komi_on = False
        # else:
        #     game.komi = float(komi_input)
        #     player2.score += game.komi
        self.game.komi = 6.5 # for testing, remove and uncomment above, later
        self.game.players[1].score += self.game.komi


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
    engine = GameEngine()
    engine.play_game()
