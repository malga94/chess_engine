# -*- coding: utf-8 -*-
"""
Trying to build a working chess engine

@author: fmalgarini
"""

from modules.legal_moves import *
from modules.support_func import *
import numpy as np

all_pieces = ['b,r', 'b,k', 'b,b', 'b,q', 'b,K', 'b,p', 'w,r', 'w,k', 'w,b', 'w,q', 'w,K', 'w,p']

def initialize_starting_position():

    starting_position = np.chararray((8, 8), unicode = True, itemsize = 3)

    for i in range(2, 6):
        for j in range(0, 8):
            starting_position[i][j] = "emp"

    for i in range(0, 8):
        starting_position[1][i] = "b,p"
        starting_position[6][i] = "w,p"

    starting_position[0][0], starting_position[0][7] = "b,r", "b,r"
    starting_position[0][1], starting_position[0][6] = "b,k", "b,k"
    starting_position[0][2], starting_position[0][5] = "b,b", "b,b"
    starting_position[0][3] = "b,q"
    starting_position[0][4] = "b,K"

    starting_position[7][0], starting_position[7][7] = "w,r", "w,r"
    starting_position[7][1], starting_position[7][6] = "w,k", "w,k"
    starting_position[7][2], starting_position[7][5] = "w,b", "w,b"
    starting_position[7][3] = "w,q"
    starting_position[7][4] = "w,K"

    return starting_position

def check_valid_coord(st_pos, end_pos):

    x_st, y_st = st_pos[1], st_pos[0]
    x_end, y_end = end_pos[1], end_pos[0]

    if 0 <= x_st < 8 and 0 <= y_st < 8:
        pass
    else:
        print("Please insert a valid starting coordinate. It must be between 0 and 7 included")
        return False

    if 0 <= x_end < 8 and 0 <= y_end < 8:
        pass
    else:
        print("Please insert a valid arrival coordinate. It must be between 0 and 7 included")
        return False

    return True

def main():
    print("Welcome to TerribleChess! Press q in any moment to quit the game")
    is_valid = False

    player = {"w":0, "b":1}

    initial_pos = initialize_starting_position()
    print(initial_pos)

    while is_valid == False:

        position = initial_pos
        piece = 'emp'

        #TODO: write code that cheks input is in the right format, which is two integer coordinates separated by a comma
        while piece == 'emp':
            st_pos = input("Insert the coordinates of the piece you want to move: ").split(',')
            try:
                st_pos = list(map(int, st_pos))
            except:
                exit()
            if check_valid_coord(st_pos, [0,0]):
                piece = position[st_pos[0]][st_pos[1]]
            if piece == 'emp':
                print("There is no piece in the given coordinate.")
            if piece[0] == 'b':
                print("You are playing with white.")
                piece = 'emp'

        while True:
            end_pos = input("Insert the coordinates of the destination of the piece: ").split(',')
            try:
                end_pos = list(map(int, end_pos))
            except:
                exit()
            if check_valid_coord(st_pos, end_pos):
                break

        #colour = 0 if white, 1 if black
        colour = player[piece[0]]

        if piece[2] == 'r':
            is_valid = rook_move(position, st_pos, end_pos, colour)
        elif piece[2] == 'k':
            is_valid = knight_move(position, st_pos, end_pos, colour)
        elif piece[2] == 'b':
            is_valid = bishop_move(position, st_pos, end_pos, colour)
        elif piece[2] == 'q':
            is_valid = queen_move(position, st_pos, end_pos, colour)
        elif piece[2] == 'K':
            is_valid = king_move(position, st_pos, end_pos, colour)
        elif piece[2] == 'p':
            is_valid = pawn_move(position, st_pos, end_pos, colour)
        else:
            print("Error. Quitting program...")
            exit()

    if is_valid:
        print("Non ho ancora codato questa parte haha")

if __name__ == '__main__':
    main()
