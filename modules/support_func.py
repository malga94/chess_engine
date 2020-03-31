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

point_dict = {'r':5, 'k':3, 'b':3, 'q':9, 'K':100, 'p':1}
player = {"w":0, "b":1}
possible_moves_l = []
points_tree = []

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

def calc_points(position, move_num):

    points_w = 0
    points_b = 0
    for i in range(0,8):
        for j in range(0,8):
            if position[i][j] == 'emp':
                continue
            elif position[i][j][0] == 'w':
                if position[i][j] == 'w,k' and move_num > 7:
                    if i%7 == 0 or j%7 == 0:
                        points_w += 2.5
                    elif 2<=i<=5 and 2<=j<=5:
                        points_w += 3.5
                    else:
                        points_w += point_dict[position[i][j][2]]
                else:
                    points_w += point_dict[position[i][j][2]]
            elif position[i][j][0] == 'b':
                if position[i][j] == 'b,k' and move_num > 7:
                    if i%7 == 0 or j%7 == 0:
                        points_b += 2.5
                    elif 2<=i<=5 and 2<=j<=5:
                        points_b += 3.5
                    else:
                        points_b += point_dict[position[i][j][2]]
                elif position[i][j] == 'b,b' and move_num > 7:
                    bishop_val = check_diagonals(position, i, j)
                    points_b += bishop_val
                elif position[i][j] == 'b,r' and move_num < 10:
                    #Slightly discouraging movement of rooks in the first 10 moves
                    if i != 0 or j%7 != 0:
                        points_b += 4.5
                    else:
                        points_b += 5
                else:
                    points_b += point_dict[position[i][j][2]]

    return points_w, points_b

def check_diagonals(position, i, j):
    #Function to assign a value to the bishop as a function of how many pieces lie on the check_diagonals
    #controlled by it. The reasoning is that a bishop controlling an empty diagonal is more valuable, and
    #moves leading to such a position should be encouraged

    #Total pieces on the board
    total_pieces = -1
    diagonals = []
    #Put every square covered by the bishop in (i,j) in the array diagonals
    for x in range(0,8):
        for y in range(0,8):
            if abs(i-y) == abs(j-x):
                diagonals.append((y,x))
            if position[y][x] != 'emp':
                total_pieces += 1

    #Remove the square occupied by the bishop from diagonals
    diagonals.remove((i,j))

    num_pieces = 0
    for pos in diagonals:
        #count the number of pieces in the diagonals controlled by the bishop
        if position[pos[0]][pos[1]] != 'emp':
            num_pieces += 1

    bishop_val = 3.5-5*num_pieces/total_pieces

    return bishop_val

def updatepos(position, st_pos, end_pos, colour, piece):

    temp_position = position.copy()
    x_st, y_st = int(st_pos[1]), int(st_pos[0])
    x_end, y_end = int(end_pos[1]), int(end_pos[0])

    temp_position[y_st][x_st] = "emp"
    temp_position[y_end][x_end] = piece

    return temp_position

def calculate_next_move(position, colour, depth, cont, move_num):

    global possible_moves_l
    if depth == cont:
        possible_moves_l = []
    if colour == 0:
        c = 'w'
    else:
        c = 'b'

    all_positions = [(x,y) for x in range(0,8) for y in range(0,8)]
    possible_starting_positions = [(x,y) for x in range(0,8) for y in range(0,8) if position[x][y][0] == c]

    for st_pos in possible_starting_positions:
        piece = position[st_pos[0]][st_pos[1]]

        for end_pos in all_positions:

            if check_move(piece, position, st_pos, end_pos, colour, 1):

                temp_position = updatepos(position, st_pos, end_pos, colour, piece)
                points_w, points_b = calc_points(temp_position, move_num)
                possible_moves_l.append([st_pos, end_pos, c, cont, points_b-points_w])
                if cont > 1:
                    calculate_next_move(temp_position, int(not colour), depth, cont-1, move_num)

    return possible_moves_l

def pack_list(possible_moves, depth, x):

    if depth not in [1,2,3,4]:
        print("Warning: pack_list function only works for depths up to 4. Returning empy list")
        return []

    first_layer, second_layer, third_layer, fourth_layer = [], [], [], []
    for i in range(depth - 1, x):
        if possible_moves[i][3] == 1:
            first_layer.append(possible_moves[i][4])
        elif possible_moves[i][3] == 2 and possible_moves[i-1][3] != 3:
            second_layer.append(first_layer)
            first_layer = []
        elif possible_moves[i][3] == 3 and possible_moves[i-1][3] != 4:
            second_layer.append(first_layer)
            third_layer.append(second_layer)
            first_layer = []
            second_layer = []
        elif possible_moves[i][3] == 4:
            second_layer.append(first_layer)
            third_layer.append(second_layer)
            fourth_layer.append(third_layer)
            first_layer = []
            second_layer = []
            third_layer = []

    if depth == 1:
        return first_layer
    elif depth == 2:
        second_layer.append(first_layer)
        return second_layer
    elif depth == 3:
        second_layer.append(first_layer)
        third_layer.append(second_layer)
        return third_layer
    elif depth == 4:
        second_layer.append(first_layer)
        third_layer.append(second_layer)
        fourth_layer.append(third_layer)
        return fourth_layer

def extract_max_list_of_tuples(list_of_tuples):

    a = []
    for i in list_of_tuples:
        a.append(i[1])

    greatest = max(a)
    max_vals = []
    for i, val in enumerate(a):
        if val == greatest:
            max_vals.append(i)

    maxval = list_of_tuples[random.choice(max_vals)][0]
    return maxval

def extract_max_from_dict(best_move_dict):

    maxval = max(best_move_dict.values())
    good_keys = []
    for key in best_move_dict:
        if best_move_dict[key] == maxval:
            good_keys.append(key)

    return random.choice(good_keys)

def choose_best_move(possible_moves, depth):

    cont = depth
    indexes = [[] for i in range(depth)]
    while cont > 0:
        for i, move in enumerate(possible_moves):
            if move[3] == cont:
                indexes[cont-1].append(i)

        cont = cont - 1

    x = len(possible_moves)
    packed_moves = pack_list(possible_moves, depth, x)

    best_move = []
    best_move_dict = {}
    cont = 0

    if depth == 1:
        for i, val in enumerate(packed_moves):
            if val == max(packed_moves):
                best_move.append(i)

        chosen_move = possible_moves[random.choice(best_move)]
        return chosen_move

    for i, layer in enumerate(packed_moves):
        if depth > 2:
            best_move.append({})
            for j, second_layer in enumerate(layer):
                if depth > 3:
                    for k, third_layer in enumerate(second_layer):
                        exit()
                else:
                    maxval = max(second_layer)
                    pos = indexes[depth-2][cont] + second_layer.index(maxval) + 1

                    best_move[i].update({pos:maxval})
                    cont += 1
        else:
            minval = min(layer)
            pos = indexes[depth-1][cont] + layer.index(minval) + 1
            best_move_dict.update({pos:minval})
            cont += 1

    if depth == 2:
        best_move_pos = extract_max_from_dict(best_move_dict)

    if depth > 2:
        temp = []
        for dict in best_move:
            temp.append(min(dict.items(), key=lambda x: x[1]))

        #Here we need to extract all positions in the temp list where the points are maximum
        for i, val in enumerate(temp):
            print(possible_moves[val[0]])
            print(best_move[i])
            for index in reversed(indexes[depth-1]):
                if val[0] > index:
                    print(possible_moves[index])
                    print("\n")
                    break
        best_move_pos = extract_max_list_of_tuples(temp)

    for index in reversed(indexes[depth-1]):
        if best_move_pos > index:
            chosen_move = possible_moves[index]
            break

    return chosen_move

def is_in_check(position, colour, move_num):
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

    possible_moves = calculate_next_move(position, int(not colour), 1, 1, move_num)

    for move in possible_moves:
        if str(move)[9:15] == str(king_pos):
            return True

    return False

def handle_check(position, colour, move_num):
    game_over = True
    alm_list, alm_points_list = [], []

    possible_moves = calculate_next_move(position, colour, 1, 1, move_num)

    temp_position = position.copy()

    if is_in_check(temp_position, colour, move_num):

        for legal_move in possible_moves:

            move = legal_move[0:2]
            piece = position[move[0][0]][move[0][1]]
            st_pos, end_pos = move[0], move[1]
            temp_position = updatepos(position, st_pos, end_pos, colour, piece)
            if not is_in_check(temp_position, colour, move_num):
                game_over = False

                points_w, points_b = calc_points(temp_position, move_num)
                points = points_b - points_w

                alm_list.append(move)
                alm_points_list.append(points)

    #TODO: Here it only looks one move ahead, so it always captures if possible. Of course,
    #it is not always the best move, especially when one is in check (for now if there is a mate
    #in 2 where the first move is the computer taking a piece, and it could easily be avoided by
    #not taking, the computer will always take because it only "sees" one move ahead)
    move_to_do = [i for i, val in enumerate(alm_points_list) if val == max(alm_points_list)]
    move = alm_list[random.choice(move_to_do)]

    piece = position[move[0][0]][move[0][1]]

    if game_over:
        if colour == 0:
            player = "white"
        else:
            player = "black"
        print("Game over: {0} wins!".format(player))
        exit()

    return move, piece

def castle(position, short, colour):

    temp_position = position.copy()

    if short and not colour:
        temp_position[7][5] = "w,r"
        temp_position[7][6] = "w,K"
        temp_position[7][4] = "emp"
        temp_position[7][7] = "emp"

    elif short and colour:
        temp_position[0][5] = "b,r"
        temp_position[0][6] = "b,K"
        temp_position[0][4] = "emp"
        temp_position[0][7] = "emp"

    elif not short and not colour:
        temp_position[7][2] = "w,r"
        temp_position[7][3] = "w,K"
        temp_position[7][4] = "emp"
        temp_position[7][0] = "emp"

    else:
        temp_position[0][3] = "b,r"
        temp_position[0][2] = "b,K"
        temp_position[0][4] = "emp"
        temp_position[0][0] = "emp"

    return temp_position

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
