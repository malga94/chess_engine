# -*- coding: utf-8 -*-
"""
Support functions for chess engine

@author: fmalgarini
"""
from modules.legal_moves import *
import numpy as np
import random

point_dict = {'r':5, 'k':3, 'b':3, 'q':9, 'K':0, 'p':1}

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

def check_move(piece, position, st_pos, end_pos, colour, turn):

        if piece[2] == 'r':
            is_valid = rook_move(position, st_pos, end_pos, colour, turn)
        elif piece[2] == 'k':
            is_valid = knight_move(position, st_pos, end_pos, colour, turn)
        elif piece[2] == 'b':
            is_valid = bishop_move(position, st_pos, end_pos, colour, turn)
        elif piece[2] == 'q':
            is_valid = queen_move(position, st_pos, end_pos, colour, turn)
        elif piece[2] == 'K':
            is_valid = king_move(position, st_pos, end_pos, colour, turn)
        elif piece[2] == 'p':
            is_valid = pawn_move(position, st_pos, end_pos, colour, turn)
        else:
            print("Error. Quitting program...")
            exit()

        return is_valid

def prepare_move(possible_moves):

    min_points = min(possible_moves.items())[1]
    min_keys = [k for k in possible_moves if possible_moves[k] == min_points]

    move = list(random.choice(min_keys))
    chars_to_remove = "( )[],'"
    for c in chars_to_remove:
        move = [x for x in move if x != c]
    
    piece = str(move[4]) + ',' + str(move[5])
    move = [(move[0], move[1]), (move[2], move[3])]

    return move, piece

def calc_points(position):

    points_w = 0
    points_b = 0
    for i in range(0,8):
        for j in range(0,8):
            if position[i][j] == 'emp':
                break
            elif position[i][j][0] == 'w':
                points_w += point_dict[position[i][j][2]]
            elif position[i][j][0] == 'b':
                points_b += point_dict[position[i][j][2]]

    return points_w, points_b

def updatepos(position, st_pos, end_pos, colour, piece):

    temp_position = position.copy()
    x_st, y_st = int(st_pos[1]), int(st_pos[0])
    x_end, y_end = int(end_pos[1]), int(end_pos[0])

    temp_position[y_st][x_st] = "emp"
    temp_position[y_end][x_end] = piece

    return temp_position
