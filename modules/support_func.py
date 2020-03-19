# -*- coding: utf-8 -*-
"""
Support functions for chess engine

@author: fmalgarini
"""
import random
import glob
import os
import numpy as np
from modules.legal_moves import *

point_dict = {'r':5, 'k':3, 'b':3, 'q':9, 'K':0, 'p':1}
player = {"w":0, "b":1}

def read_settings():

    with open("./settings.txt", "r") as f:
        data = f.readlines()

    try:
        depth = int(data[0][-2:-1])
    except:
        print("Warning: check syntax of settings file when defining depth")

    try:
        load = data[1][-2:-1]
    except:
        print("Warning: check syntax of settings file when defining load")

    return depth, load

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

def load_starting_position(game_num):

    with open("./saved_games/game{0}.txt".format(game_num), 'r') as f:
        data = f.read()

    data = data.splitlines()

    starting_position = np.chararray((8, 8), unicode = True, itemsize = 3)
    for i in range(0,8):
        for j in range(0,8):
            starting_position[i][j] = data[i][6*j+3:6*j+6]

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

def prepare_move_depth_1(possible_moves, randomness):

    min_points = min(possible_moves.items())[1]
    min_keys = [k for k in possible_moves if possible_moves[k] == min_points]

    if randomness == -1:
        move = list(random.choice(min_keys))
    elif 0 <= randomness < len(min_keys):
        move = list(min_keys[randomness])
    else:
        print("""Warning: something wrong in the prepare_move_depth_1 function. Please send
              this message to filippo.malgarini@gmail.com together with the last position on screen""")
        randomness = 0
        move = list(min_keys[randomness])

    chars_to_remove = "( )[],'"
    for c in chars_to_remove:
        move = [x for x in move if x != c]

    piece = str(move[4]) + ',' + str(move[5])
    move = [(move[0], move[1]), (move[2], move[3])]

    return move, piece

def prepare_move_depth_2(possible_moves, position):

    move = possible_moves.split('|')[1].replace("'First move: ', ", "")
    piece = position[int(move[2])][int(move[5])]
    move = [(move[2], move[5]), (move[10], move[13])]

    return move, piece

def calc_points(position):

    points_w = 0
    points_b = 0
    for i in range(0,8):
        for j in range(0,8):
            if position[i][j] == 'emp':
                continue
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

def compute_legal_moves(position, colour, recall):

    cont = 0
    possible_moves = {}
    possible_second_moves = []
    if colour == 0:
        c = 'w'
    else:
        c = 'b'

    all_positions = [(x,y) for x in range(0,8) for y in range(0,8)]
    possible_starting_positions = [(x,y) for x in range(0,8) for y in range(0,8) if position[x][y][0] == c]
    for st_pos in possible_starting_positions:
        piece = position[st_pos[0]][st_pos[1]]

        if piece == 'emp':
            break
        for end_pos in all_positions:

            if check_move(piece, position, st_pos, end_pos, colour, 1):
                temp_position = updatepos(position, st_pos, end_pos, colour, piece)

                if recall != 0:

                    possible_second_moves.append(["First move: ", st_pos, end_pos])
                    possible_second_moves.append(compute_legal_moves(temp_position, int(not colour), 0))

                points_w, points_b = calc_points(temp_position)
                tentative_pos = [st_pos, end_pos, piece]
                possible_moves.update({str(tentative_pos):points_b - points_w})
            else:
                continue

    best_moves = []

    if recall:
        for moves in range(1, len(possible_second_moves), 2):
            temp = {}
            for second_moves in possible_second_moves[moves].keys():
                points = possible_second_moves[moves][second_moves]
                temp.update({str(second_moves) + "|" + str(possible_second_moves[moves-1]):points})

            best_moves.append(min(temp, key=temp.get))
            best_moves.append(temp[min(temp, key=temp.get)])
        best_moves_points = [i for i in best_moves if isinstance(i, int)]
        maxval = max(best_moves_points)
        indices = [index for index, val in enumerate(best_moves_points) if val == maxval]
        chosen_move = best_moves[random.choice(indices) * 2]
        possible_moves = chosen_move

    return possible_moves

def is_in_check(position, colour):
    x, y = 0, 0
    for square in position:
        y = 0
        for element in square:
            if colour == 1:
                if str(element) == 'b,K':
                    king_pos = (x, y)
            elif colour == 0:
                if str(element) == 'w,K':
                    king_pos = (x, y)
            y += 1
        x += 1

    possible_moves = compute_legal_moves(position,int(not colour),0)

    for move in possible_moves.keys():
        if move[-14:-8] == str(king_pos):
            return True

    return False

def get_king_moves(possible_moves):

    keys_to_pop = []
    temp_possible_moves = possible_moves.copy()
    for key in temp_possible_moves.keys():
        if key[-3] != 'K':
            keys_to_pop.append(key)

    for key in keys_to_pop:
        temp_possible_moves.pop(key, 'None')

    return temp_possible_moves

def try_blocking_check(legal_move):

    chars_to_remove = "( )[],'"

    for c in chars_to_remove:
        legal_move = [x for x in legal_move if x != c]
        #TODO: Why doesn't it work if i call move = [x for x...] in the line above?

    move = legal_move
    piece = str(move[4]) + ',' + str(move[5])
    move = [(move[0], move[1]), (move[2], move[3])]

    return move, piece

def handle_check(position, colour):
    game_over = True

    possible_moves = compute_legal_moves(position, colour, 0)
    king_moves = get_king_moves(possible_moves)
    cont = 0

    if len(king_moves) != 0:
        while cont < len(king_moves):
            move, piece = prepare_move_depth_1(king_moves, cont)
            st_pos, end_pos = move[0], move[1]

            temp_position = updatepos(position, st_pos, end_pos, colour, piece)
            cont += 1

            if not is_in_check(temp_position, colour):
                game_over = False
                break

    temp_position = position.copy()
    if cont == len(king_moves):

        if is_in_check(temp_position, colour):
            for legal_move in possible_moves:

                move, piece = try_blocking_check(legal_move)
                st_pos, end_pos = move[0], move[1]
                temp_position = updatepos(temp_position, st_pos, end_pos, colour, piece)
                if not is_in_check(temp_position, colour):

                    game_over = False
                    break

    if game_over:
        if colour == 0:
            player = "white"
        else:
            player = "black"
        print("Game over: {0} wins!".format(player))
        exit()

    return move, piece

def save_position(position):

    dir = os.listdir("./")
    if "saved_games" not in dir:
        os.mkdir("saved_games")

    files_present = glob.glob("./saved_games/*.txt")
    x = len(files_present) + 1

    if x<100:
        with open("./saved_games/game{0}.txt".format(x), "w+") as f:
            f.writelines(str(position) + '\n')

def pretty_print(pos):

    cont = 1
    for line in pos:
        for element in line:
            if element[2] == 'q':
                if cont % 8 == 0:
                    print("\033[1;31;42m {0}".format(element), end = ' ')
                    print("\033[1;37;40m")

                else:
                    print("\033[1;31;42m {0}".format(element), end = ' ')
            elif element[2] == 'b':
                if cont % 8 == 0:
                    print("\033[1;32;40m {0}".format(element), end = ' ')
                    print("\033[1;37;40m")

                else:
                    print("\033[1;32;40m {0}".format(element), end = ' ')
            elif element[2] == 'k':
                if cont % 8 == 0:
                    print("\033[1;33;40m {0}".format(element), end = ' ')
                    print("\033[1;37;40m")

                else:
                    print("\033[1;33;40m {0}".format(element), end = ' ')
            elif element[2] == 'r':
                if cont % 8 == 0:
                    print("\033[1;34;47m {0}".format(element), end = ' ')
                    print("\033[1;37;40m")

                else:
                    print("\033[1;34;47m {0}".format(element), end = ' ')
            elif element[2] == 'K':
                if cont % 8 == 0:
                    print("\033[1;35;40m {0}".format(element), end = ' ')
                    print("\033[1;37;40m")

                else:
                    print("\033[1;35;40m {0}".format(element), end = ' ')
            elif element[2] == 'p':
                if cont % 8 == 0:
                    print("\033[1;37;40m {0}".format(element))

                else:
                    print("\033[1;37;40m {0}".format(element), end = ' ')
            else:
                if cont % 8 == 0:
                    print("\033[1;37;40m ")

                else:
                    print("\033[1;37;40m ", end = ' ')
            cont += 1
    print("\033[1;37;40m")
