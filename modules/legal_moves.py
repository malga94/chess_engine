# -*- coding: utf-8 -*-
"""
Functions to determine if a chess move is legal

@author: fmalgarini
"""

w_king_moved, b_king_moved = False, False
w_rook1_moved, w_rook2_moved, b_rook1_moved, b_rook2_moved = False, False, False, False

def check_empty_path(position, x_st, y_st, x_end, y_end, turn):

    if x_st == x_end:
        if y_st < y_end:
            for i in range(y_st+1, y_end):
                if position[i][x_st] != 'emp':
                    if turn == 0:
                        print("There is another piece in the way. Try another move")
                    return False

        else:
            for i in range(y_st-1, y_end, -1):
                if position[i][x_st] != 'emp':
                    if turn == 0:
                        print("There is another piece in the way. Try another move")
                    return False

    elif y_st == y_end:
        if x_st < x_end:
            for i in range(x_st+1, x_end):
                if position[y_st][i] != 'emp':
                    if turn == 0:
                        print("There is another piece in the way. Try another move")
                    return False

        else:
            for i in range(x_st-1, x_end, -1):
                if position[y_st][i] != 'emp':
                    if turn == 0:
                        print("There is another piece in the way. Try another move")
                    return False

    else:
        if x_st < x_end:
            if y_st < y_end:
                for i in range(x_st+1, x_end):
                    if position[i+y_st-x_st][i] != 'emp':
                        if turn == 0:
                            print("There is another piece in the way. Try another move")
                        return False

            else:
                for i in range(x_st+1, x_end):
                    if position[y_st+x_st-i][i] != 'emp':
                        if turn == 0:
                            print("There is another piece in the way. Try another move")
                        return False

        elif x_st > x_end:
            if y_st < y_end:
                for i in range(x_st-1, x_end, -1):
                    if position[x_st+y_st-i][i] != 'emp':
                        if turn == 0:
                            print("There is another piece in the way. Try another move")
                        return False
            else:
                for i in range(x_st-1, x_end, -1):
                    if position[i-x_st+y_st][i] != 'emp':
                        if turn == 0:
                            print("There is another piece in the way. Try another move")
                        return False

    return True

def rook_move(position, st_pos, end_pos, colour, turn):

    global rook1_moved, rook2_moved

    x_st, y_st = st_pos[1], st_pos[0]
    x_end, y_end = end_pos[1], end_pos[0]

    if colour == 0:
        if position[y_st][x_st] != "w,r":
            print("Error: there is a bug in the code. Please write a mail to filippo.malgarini@gmail.com with a screenshot of the position and the move you just tried to play")
            return False
        if position[y_end][x_end][0] == 'w': #The arrival position has a white piece on it
            if turn == 0:
                print("Warning: there is a white piece already in the arrival position. Try another move")
            return False

    if colour == 1:
        if position[y_st][x_st] != "b,r":
            return False
        if position[y_end][x_end][0] == 'b': #The arrival position has a black piece on it
            if turn == 0:
                print("Warning: there is a black piece already in the arrival position. Try another move")
            return False

    if x_st == x_end and y_st == y_end:
        return False

    elif x_st != x_end and y_st != y_end:
        return False

    if turn == 0:
        if x_st == 0 and y_st == 0:
            b_rook1_moved = True

        if x_st == 7 and y_st == 0:
            b_rook2_moved = True

        if x_st == 0 and y_st == 7:
            w_rook1_moved = True

        if x_st == 7 and y_st == 7:
            w_rook2_moved = True

    return check_empty_path(position, x_st, y_st, x_end, y_end, turn)

def knight_move(position, st_pos, end_pos, colour, turn):

    x_st, y_st = st_pos[1], st_pos[0]
    x_end, y_end = end_pos[1], end_pos[0]

    if colour == 0:
        if position[y_st][x_st] != "w,k":
            print("Error: there is a bug in the code. Please write a mail to filippo.malgarini@gmail.com with a screenshot of the position and the move you just tried to play")
            return False
        if position[y_end][x_end][0] == 'w': #The arrival position has a white piece on it
            if turn == 0:
                print("Warning: there is a white piece already in the arrival position. Try another move")
            return False

    if colour == 1:
        if position[y_st][x_st] != "b,k":
            return False
        if position[y_end][x_end][0] == 'b': #The arrival position has a black piece on it
            if turn == 0:
                print("Warning: there is a black piece already in the arrival position. Try another move")
            return False

    if (abs(y_end-y_st) == 2 and abs(x_end-x_st) == 1) or (abs(y_end-y_st) == 1 and abs(x_end-x_st) == 2):
        return True

    if turn == 0:
        print("That's not how the knight moves! Try another move")
    return False

def bishop_move(position, st_pos, end_pos, colour, turn):

    x_st, y_st = st_pos[1], st_pos[0]
    x_end, y_end = end_pos[1], end_pos[0]

    if colour == 0:
        if position[y_st][x_st] != "w,b":
            print("Error: there is a bug in the code. Please write a mail to filippo.malgarini@gmail.com with a screenshot of the position and the move you just tried to play")
            return False
        if position[y_end][x_end][0] == 'w': #The arrival position has a white piece on it
            if turn == 0:
                print("Warning: there is a white piece already in the arrival position. Try another move")
            return False

    if colour == 1:
        if position[y_st][x_st] != "b,b":
            return False
        if position[y_end][x_end][0] == 'b': #The arrival position has a black piece on it
            if turn == 0:
                print("Warning: there is a black piece already in the arrival position. Try another move")
            return False

    if abs(x_st-x_end) != abs(y_st-y_end):
        if turn == 0:
            print("That's not how the bishop moves! Try another move")
        return False

    return check_empty_path(position, x_st, y_st, x_end, y_end, turn)

def queen_move(position, st_pos, end_pos, colour, turn):

    x_st, y_st = st_pos[1], st_pos[0]
    x_end, y_end = end_pos[1], end_pos[0]

    if colour == 0:
        if position[y_st][x_st] != "w,q":
            print("Error: there is a bug in the code. Please write a mail to filippo.malgarini@gmail.com with a screenshot of the position and the move you just tried to play")
            return False
        if position[y_end][x_end][0] == 'w': #The arrival position has a white piece on it
            if turn == 0:
                print("Warning: there is a white piece already in the arrival position. Try another move")
            return False

    if colour == 1:
        if position[y_st][x_st] != "b,q":
            return False
        if position[y_end][x_end][0] == 'b': #The arrival position has a black piece on it
            if turn == 0:
                print("Warning: there is a black piece already in the arrival position. Try another move")
            return False

    if abs(x_st-x_end) != abs(y_st-y_end) and (x_st != x_end and y_st != y_end):
        if turn == 0:
            print("That's not how the queen moves! Try another move")
        return False

    return check_empty_path(position, x_st, y_st, x_end, y_end, turn)

def king_move(position, st_pos, end_pos, colour, turn):

    global w_king_moved, b_king_moved, w_rook1_moved, w_rook2_moved, b_rook1_moved, b_rook2_moved

    x_st, y_st = st_pos[1], st_pos[0]
    x_end, y_end = end_pos[1], end_pos[0]

    if colour == 0:

        #Short castle
        if position[y_end][x_end] == "w,r":
            if w_king_moved == False and w_rook2_moved == False:
                return check_empty_path(position, x_st, y_st, x_end, y_end, turn)
            else:
                if turn == 0:
                    print("Cannot castle: the white king has already moved")
                return False

        #Long castle
        if position[y_end][x_end] == "w,r":
            if w_king_moved == False and w_rook1_moved == False:
                return check_empty_path(position, x_st, y_st, x_end, y_end, turn)
            else:
                if turn == 0:
                    print("Cannot castle: the white king has already moved")
                return False

        if position[y_st][x_st] != "w,K":
            print("Error: there is a bug in the code. Please write a mail to filippo.malgarini@gmail.com with a screenshot of the position and the move you just tried to play")
            return False
        if position[y_end][x_end][0] == 'w': #The arrival position has a white piece on it
            if turn == 0:
                print("Warning: there is a white piece already in the arrival position. Try another move")
            return False

    if colour == 1:
        #Short castle
        if position[y_end][x_end] == "b,r":
            if b_king_moved == False and b_rook2_moved == False:
                return check_empty_path(position, x_st, y_st, x_end, y_end, turn)
            else:
                return False

        #Long castle
        if position[y_end][x_end] == "b,r":
            if b_king_moved == False and b_rook1_moved == False:
                return check_empty_path(position, x_st, y_st, x_end, y_end, turn)
            else:
                return False

        if position[y_st][x_st] != "b,K":
            return False
        if position[y_end][x_end][0] == 'b': #The arrival position has a black piece on it
            if turn == 0:
                print("Warning: there is a black piece already in the arrival position. Try another move")
            return False

    if abs(x_end-x_st) > 1 or abs(y_end-y_st) > 1:
        if turn == 0:
            print("That's not how the king moves! Try another move")
        return False

    if turn == 0:
        if colour == 0:
            w_king_moved = True
        else:
            b_king_moved = True

    return True

def pawn_move(position, st_pos, end_pos, colour, turn):

    x_st, y_st = st_pos[1], st_pos[0]
    x_end, y_end = end_pos[1], end_pos[0]

    if colour == 0:
        if position[y_st][x_st] != "w,p":
            print("Error: there is a bug in the code. Please write a mail to filippo.malgarini@gmail.com with a screenshot of the position and the move you just tried to play")
            return False
        if position[y_end][x_end][0] == 'w': #The arrival position has a white piece on it
            if turn == 0:
                print("Warning: there is a white piece already in the arrival position. Try another move")
            return False

        elif position[y_end][x_end] == 'emp':
            if y_st == 6:
                 if x_end != x_st or (y_end != y_st - 1 and y_end != y_st - 2):

                     if turn == 0:
                         print("That's not how the pawn moves! Try another move")
                     return False

            else:
                 if x_end != x_st or y_end != y_st - 1:
                     if turn == 0:
                         print("That's not how the pawn moves! Try another move")
                     return False

        else:
            if abs(x_end - x_st) != 1 or y_end != y_st - 1:
                if turn == 0:
                    print("That's not how the pawn moves! Try another move")
                return False

    if colour == 1:
        if position[y_st][x_st] != "b,p":
            print(f"Position: {y_st}{x_st}, \n{position}")
            print("Error: there is a bug in the code. Please write a mail to filippo.malgarini@gmail.com with a screenshot of the position and the move you just tried to play")
            return False
        if position[y_end][x_end][0] == 'b': #The arrival position has a white piece on it
            if turn == 0:
                print("Warning: there is a black piece already in the arrival position. Try another move")
            return False

        elif position[y_end][x_end] == 'emp':
            if y_st == 1:
                 if x_end != x_st or (y_end != y_st + 1 and y_end != y_st + 2):
                     if turn == 0:
                         print("That's not how the pawn moves! Try another move")
                     return False

            else:
                 if x_end != x_st or y_end != y_st + 1:
                     if turn == 0:
                         print("That's not how the pawn moves! Try another move")
                     return False

        else:
            if abs(x_end - x_st) != 1 or y_end != y_st + 1:
                if turn == 0:
                    print("That's not how the pawn moves! Try another move")
                return False

    return True
