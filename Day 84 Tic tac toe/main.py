def display_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]} ")

def check_win(board, player):

    win_conditions = [

        [0, 1, 2], [3, 4, 5], [6, 7, 8],

        [0, 3, 6], [1, 4, 7], [2, 5, 8],

        [0, 4, 8], [2, 4, 6]

    ]
    for con in win_conditions:
        if all(board[i] == player for i in con):
            return True
    return False



def draw(board):
    return all(cell in ["X", "O"] for cell in board)


def play_game():
    board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    cur_player = "X"
    game_status = True
    print("Welcome to Tic Tac Toe!")
    display_board(board)
    while game_status:
        move_in = input(f"Player has {cur_player},choose between 1-9: ")
        if not move_in.isdigit():
            print("Invalid input. Please enter a number.")
            continue
        move = int(move_in)
        if  move < 1 or move > 9:
            print("Invalid input. Please choose a number between 1 and 9.")

            continue
        move_ind = move - 1
        if board[move_ind] in ["X", "O"]:
            print("That position is already taken. Choose another.")

            continue
        board[move_ind] = cur_player
        display_board(board)

        if check_win(board, cur_player):
            print(f"Player {cur_player} wins!")
            game_status = False

        elif draw(board):

            print("It's a draw!")

            game_status = False

        else:

            cur_player = "O" if cur_player == "X" else "X"


play_game()




