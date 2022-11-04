import pygame
from Engine_class import *
board = create_board()  # Creation of the board and print in the console
print_board(board)

game_over = False
turn = 0  # The player 1 starts
print(turn)
pygame.init()
choice = int(input("Select 1 for 2 players or select 2 to play vs the AI: "))

if choice != 1 and choice != 2:  # If number not valid
    print("Not valid number")
    choice = int(input("Select 1 for 2 players or select 2 to play vs the AI: "))


# Choice for 2 players
if choice == 1:
    while not game_over:  # While loop that runs until the game is over
        if turn == 0:  # Turn of the player
            print("Player 1, your turn!!")
            num = int(input("Select column: ")) - 1  # -1 for eliminating the starting point from 0
            if free_location(board, num):  # Check the location of the column selected
                row = next_free_row(board, num)
                set_value(board, row, num, 1)  # change the value of the free position
                print_board(board)
                if backtrack_algorithm_winning(board, 1):
                    print("Player 1 wins")
                    break
        else:  # Turn of the Player 2
            print("Player 2, your turn!!")
            num = int(input("Select column: ")) - 1
            if free_location(board, num):  # Check the location of the column selected
                row = next_free_row(board, num)
                set_value(board, row, num, 2)  # change the value of the free position
                print_board(board)
                if backtrack_algorithm_winning(board, 2):
                    print("Player 2 wins")
                    break

        turn += 1
        turn = turn % 2
        print(turn)


# Choice for playing vs AI
elif choice == 2:
    while not game_over:  # While loop that runs until the game is over

        if turn == 0:  # Turn of the player
            print("Player 1, your turn!!")
            num = int(input("Select column: ")) - 1  # -1 for eliminating the starting point from 0
            if free_location(board, num):  # Check the location of the column selected
                row = next_free_row(board, num)
                set_value(board, row, num, 1)  # change the value of the free position
                print_board(board)
                if backtrack_algorithm_winning(board, 1):
                    print("Player 1 wins")
                    break
        else:  # Turn of the AI
            print("AI your turn!!")
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            if free_location(board, col):
                row = next_free_row(board, col)
                set_value(board, row, col, ai_value)
                print_board(board)
                if backtrack_algorithm_winning(board, ai_value):
                    print("AI wins")
                    game_over = True

        turn += 1
        turn = turn % 2
        print(turn)
