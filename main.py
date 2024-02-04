row_alpha_dict = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8}
board = [[[] for i in range(0, 9)] for j in range(0, 9)]
exit_game = False
player_1_turn = True
players = []


def play_game():
    global exit_game
    print("Welcome to Weiqi")
    print("enter 'exit' to quit at any time")
    players.append(input("Player 1 enter name: "))
    players.append(input("Player 2 enter name: "))
    while not exit_game:
        current_player = players[not player_1_turn]
        print(current_player + "'s turn")
        print_board()
        take_move_input()


def print_board():
    global board
    for row in board:
        print(row)


def take_move_input():
    global exit_game
    global player_1_turn
    valid_move = False
    while not exit_game and not valid_move:
        move_input = input('Enter Move: ')
        if move_input == "exit":
            exit_game = True
            break
        move_row = move_input[0]
        move_col = int(move_input[1])
        valid_move = validate_move(move_row, move_col)
        if valid_move:
            player_1_turn = not player_1_turn
            print("valid move")


def validate_move(move_row, move_col):
    print(move_row, move_col)
    if move_row not in row_alpha_dict:
        return False
    return move_col in range(0, 9)


if __name__ == '__main__':
    play_game()
