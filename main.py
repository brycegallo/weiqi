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
            self.players = [GameEngine.Player('Player 1', "B"), GameEngine.Player('Player 2', "W")]
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
        def __init__(self, name, color):
            self.name = name
            self.color = color
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
        # self.print_liberties()  # for testing
        print("groups: " + str(self.count_all_groups()))

    def count_all_groups(self):
        board = self.game.current_board
        rows, cols = len(board), len(board[0])
        visited = set()
        colors = [self.game.current_player.color, self.game.waiting_player.color]
        groups = 0
        groups_list = []
        all_pieces = set()
        black_groups = 0
        black_groups_set = set()
        white_groups = 0
        white_groups_set = set()
        groups_surrounded = 0
        groups_w_liberties = 0
        black_groups_list = []
        white_groups_list = []

        def breadth_first_search(input_r, input_c, group_color):
            dqueue = collections.deque()
            visited.add((input_r, input_c))
            dqueue.append((input_r, input_c))

            # create sets to hold every piece in each group
            black_set = set()  # Scope: breadth_first_search()
            black_set_list = []
            white_set = set()  # Scope: breadth_first_search()
            # adds first coordinate to set if it's a piece, before entering deque
            if board[input_r][input_c].color == "B" and (board[input_r][input_c].color, input_r, input_c) not in black_set:
                print("added black to group")
                black_set.add((group_color, input_r, input_c))
            if board[input_r][input_c].color == "W" and (board[input_r][input_c].color, input_r, input_c) not in white_set:
                print("added white to group")
                white_set.add((group_color, input_r, input_c))
            print("before if statement")
            print(black_set_list)
            if board[input_r][input_c].color == "B" and (board[input_r][input_c].color, input_r, input_c) not in black_set_list:
                print("not in")
                black_set_list.append((group_color, input_r, input_c))

            while dqueue:
                group_liberties = 0
                q_r, q_c = dqueue.popleft()
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

                for d_r, d_c in directions:
                    r, c = q_r + d_r, q_c + d_c
                    if r in range(rows) and c in range(cols) and board[input_r][input_c] is not GameEngine.Piece:
                        group_liberties += 1
                    if (r in range(rows) and
                        c in range(cols) and
                        type(board[r][c]) is GameEngine.Piece and
                            board[r][c].color == group_color and
                            (r, c) not in visited):
                        print("r in rows, c in cols, type is piece, coordinate not visited")
                        if board[r][c].color == "B" and (board[r][c].color, r, c) not in black_set:
                            black_set.add((group_color, r, c))
                        print("before if statement")
                        print(black_set_list)
                        if board[r][c].color == "B" and (board[r][c].color, r, c) not in black_set_list:
                            print("not in")
                            black_set_list.append((group_color, r, c))
                        if board[r][c].color == "W" and (board[r][c].color, r, c) not in white_set:
                            white_set.add((group_color, r, c))
                        dqueue.append((r, c))
                        visited.add((r, c))
            if black_set_list:
                print("black set list")
                print(black_set_list)
            if black_set:
                # black_groups_list.append((black_set, group_liberties))
                black_groups_list.append(black_set)
            if white_set:
                # white_groups_list.append((white_set, group_liberties))
                white_groups_list.append(white_set)

            # def liberty_breadth_first_search():

        for group_color in colors:
            for row in range(rows):
                for column in range(cols):
                    if (type(board[row][column]) is GameEngine.Piece and
                            board[row][column].color == group_color and
                            (row, column) not in visited):
                        breadth_first_search(row, column, group_color)
                        if group_color == "B":
                            black_groups += 1
                        if group_color == "W":
                            white_groups += 1
        print("Total Groups: " + str(white_groups + black_groups))
        print("White groups: ", white_groups)
        print("Black groups: ", black_groups)
        print(black_groups_list)
        print(white_groups_list)
        # for piece in black_set:
        #     arr = [piece[0], piece[1], piece[2]]
        #     print(arr)

        return groups_list

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
