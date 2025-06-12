# Define the initial game board
board = [' ' for _ in range(9)]

# Board locations
board_locations = {
    "A1": 0,
    "B1": 1,
    "C1": 2,
    "A2": 3,
    "B2": 4,
    "C2": 5,
    "A3": 6,
    "B3": 7,
    "C3": 8,
}

# Define the possible winning combinations
wining_options = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


# Function to check if the board is full
def is_board_full(game_board):
    return ' ' not in game_board


# Function to check if a player has won
def check_winner(game_board, player):
    for row in wining_options:
        if all(game_board[i] == player for i in row):
            return True
    return False


# Minimax algorythm
def minimax(game_board, is_max, depth):
    # Player
    if check_winner(game_board=board, player="X"):
        return -1
    # AI - supported by the minimax
    elif check_winner(game_board=board, player="O"):
        return 1
    # Draw
    elif is_board_full(board):
        return 0

    if is_max:
        maximum_evaluate = -float('inf')
        for i in range(9):
            if game_board[i] == ' ':
                game_board[i] = 'O'
                evaluate = minimax(game_board=board, is_max=False, depth=depth+1)
                game_board[i] = ' '
                maximum_evaluate = max(maximum_evaluate, evaluate)
        return maximum_evaluate
    else:
        minimum_evaluate = float('inf')
        for i in range(9):
            if game_board[i] == ' ':
                game_board[i] = 'X'
                evaluate = minimax(game_board=board, is_max=True, depth=depth+1)
                game_board[i] = ' '
                minimum_evaluate = min(minimum_evaluate, evaluate)
        return minimum_evaluate


# Best move calculation with Minimax
def best_move(game_board):
    best_value = -float('inf')
    best_move_calc = None

    for i in range(9):
        if game_board[i] == ' ':
            game_board[i] = 'O'
            move_value = minimax(game_board=board, is_max=False, depth=0)
            game_board[i] = ' '
            if move_value > best_value:
                best_value = move_value
                best_move_calc = i

    return best_move_calc

# AI's move
def ai_move(game_board):
    global game_is_on
    location = best_move(game_board=board)
    game_board[location] = 'O'
    if check_winner(game_board=board, player='O'):
        print("The AI won.")
        game_is_on = False

    elif is_board_full(game_board=board):
        print("Draw!")
        game_is_on = False


# Player's move
def make_move(game_board,location, name_of_the_player):
    global game_is_on
    if game_board[location] == ' ':
        game_board[location] = 'X'
        if check_winner(game_board=board, player='X'):
            print(f"{name_of_the_player} won! Congratulation!")
            game_is_on = False

        elif is_board_full(game_board=board):
            print("Draw")
            game_is_on = False

        else:
            ai_move(game_board=board)
    else:
        print("Error", "Invalid move", "The location is not empty.")


# Start the application
print("Welcome, this is a Tic Tac Toe Game.")
print("You will play against AI which supports by minimax algorythm.")
print("Good luck and enjoy")

player_name = input("Please enter your name: ").capitalize()

if player_name == '':
    player_name = "Player"
else:
    player_name = player_name


table_draw = f"""
      | A | B | C |
    --+---+---+---+
    1 | {board[0]} | {board[1]} | {board[2]} |
    --+---+---+---+
    2 | {board[3]} | {board[4]} | {board[5]} |
    --+---+---+---+
    3 | {board[6]} | {board[7]} | {board[8]} |
    --+---+---+---+
"""
print(table_draw)


game_is_on = True
while game_is_on:
    player_location = None
    player_input = input("Please enter your location: \n").upper()
    player_input_check = True
    while player_input_check:
        try:
            player_location = board_locations[f"{player_input}"]
            player_input_check = False
        except KeyError:
            player_input = input("Invalid location. Check and reenter: \n").upper()

    make_move(game_board=board, location=player_location, name_of_the_player=player_name)

    table_draw = f"""
          | A | B | C |
        --+---+---+---+
        1 | {board[0]} | {board[1]} | {board[2]} |
        --+---+---+---+
        2 | {board[3]} | {board[4]} | {board[5]} |
        --+---+---+---+
        3 | {board[6]} | {board[7]} | {board[8]} |
        --+---+---+---+
    """
    print(table_draw)