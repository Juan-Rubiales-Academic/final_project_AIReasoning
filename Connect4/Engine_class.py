import numpy as np
import random
import math

row_count = 6
column_count = 7


def create_board():  # Create the board function
    board = np.zeros((row_count, column_count))
    return board


def set_value(board, row, col, value):  # Give a new value for the position selected
    board[row][col] = value


def free_location(board, col):  # Look the position of a free location
    if board[5][col] == 0:
        return True


def next_free_row(board, col):
    for r in range(6):
        if board[r][col] == 0:  # Find the position of the free row in the selected column
            return r


def print_board(board):
    print(np.flip(board, 0))


def backtrack_algorithm_winning(board, value):

    # We check for rows possible win
    for c in range(column_count - 3):
        for r in range(row_count):
            # Check condition for every row
            if board[r][c] == value and board[r][c + 1] == value and board[r][c + 2] == value and \
                    board[r][c + 3] == value:
                return True

    # We check for columns possible win
    for c in range(column_count):
        for r in range(row_count - 3):
            # Check condition for every column
            if board[r][c] == value and board[r + 1][c] == value and board[r + 2][c] == value and \
                    board[r + 3][c] == value:
                return True

    # We check positively diagonals win
    for c in range(column_count - 3):
        for r in range(row_count - 3):
            # Check condition for every positive diagonal
            if board[r][c] == value and board[r + 1][c + 1] == value and board[r + 2][c + 2] == value and \
                    board[r + 3][c + 3] == value:
                return True

    # We check negatively diagonals win
    for c in range(column_count - 3):
        for r in range(3, row_count):
            # Check condition for every negative diagonal
            if board[r][c] == value and board[r - 1][c - 1] == value and board[r - 2][c - 2] == value and \
                    board[r - 3][c - 3] == value:
                return True


def evaluate_window(window, piece):
    # Function for evaluating the score for the AI to select next step
    score = 0
    opp_piece = player_value
    if piece == player_value:
        opp_piece = ai_value

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(no_value) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(no_value) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(no_value) == 1:
        score -= 4

    return score


def dashboard_score(board, piece):  # Recursive algorithm to have a score dashboard
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, column_count // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(row_count):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(column_count - 3):
            window = row_array[c:c + length]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(column_count):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(row_count - 3):
            window = col_array[r:r + length]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(row_count - 3):
        for c in range(column_count - 3):
            window = [board[r + i][c + i] for i in range(length)]
            score += evaluate_window(window, piece)

    for r in range(row_count - 3):
        for c in range(column_count - 3):
            window = [board[r + 3 - i][c + i] for i in range(length)]
            score += evaluate_window(window, piece)

    return score


# AI functions

no_value = 0  # EMPTY
player_value = 1  # PLAYER_PIECE
ai_value = 2  # AI_PIECE

length = 4  # Window length


def node(board):
    return backtrack_algorithm_winning(board, player_value) or backtrack_algorithm_winning(board, ai_value) or len(
        set_location(board)) == 0


def minimax(board, depth, alpha, beta, max_player):
    # alpha beta filters through which options are unnecessary to search through in minimax

    valid_locations = set_location(board)
    terminal_valid = node(board)

    if depth == 0 or terminal_valid:
        if terminal_valid:
            if backtrack_algorithm_winning(board, ai_value):
                return None, 100000000000000
            elif backtrack_algorithm_winning(board, player_value):
                return None, -10000000000000
            else:  # Game is over, no more valid moves
                return None, 0
        else:  # Depth is zero
            return None, dashboard_score(board, ai_value)

    if max_player:  # initialize -infinity value for alpha to be compared to
        value = -math.inf
        column = random.choice(valid_locations)  # returns a randomly selected free space
        # for the AI to play in
        for col in valid_locations:  # for loop that allows the AI to select
            # its next move
            row = next_free_row(board, col)  # returns valid rows for the AI to play
            b_copy = board.copy()
            set_value(b_copy, row, col, ai_value)  # play a piece on a copy of the board
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:  # alpha then becomes the maximum value between the alpha variable
                # initialized as negative infinity, and the current best value so it is consistently updating
                break
        return column, value  # return the updated column and best values

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = next_free_row(board, col)
            b_copy = board.copy()
            set_value(b_copy, row, col, player_value)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:  # if the new play has a value lower than what is in the value
                # variable, update the column and value variables accordingly
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def set_location(board):  # Function to return a list with all the possible free locations
    list_valid = []
    for col in range(column_count):  # For all columns
        if free_location(board, col):  # Check if it has at least one free position
            list_valid.append(col)  # Add them to the list
    return list_valid


def pick_best_move(board, piece):  # Function to select the best move
    list_valid = set_location(board)  # Create the list of free locations for the board
    best_score = -10000  # Set an arbitrary score
    best_col = random.choice(list_valid)  # Select random move
    for col in list_valid:  # Check for every possible move which has the biggest score and return the best move
        row = next_free_row(board, col)
        temp = board.copy()  # Create a copy of the board to not modify the original
        set_value(temp, row, col, piece)
        score = dashboard_score(temp, piece)
        if score > best_score:  # If the col selected is greater in score, change both score and column position to best
            best_score = score
            best_col = col

    return best_col
