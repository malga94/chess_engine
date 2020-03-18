# -*- coding: utf-8 -*-
"""
Functions for the turns of player and computer

@author: fmalgarini
"""
from modules.support_func import *

player = {"w":0, "b":1}

def player_turn(position):

    is_valid = False

    while is_valid == False:

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

          is_valid = check_move(piece, position, st_pos, end_pos, colour, 0)


    position = updatepos(position, st_pos, end_pos, colour, piece)
    return position, False

def computer_turn(position, depth):

    colour = 1 #For now computer plays with black
    if depth == 1:
        possible_moves = compute_legal_moves(position, colour, 0)
        move, piece = prepare_move_depth_1(possible_moves)

    elif depth == 2:
        possible_moves = compute_legal_moves(position, colour, 1)
        move, piece = prepare_move_depth_2(possible_moves, position)

    else:
        print("Warning: depth {0} not implemented yet. Using depth = 2".format(depth))
        possible_moves = compute_legal_moves(position, colour, 1)
        move, piece = prepare_move_depth_2(possible_moves, position)

    st_pos, end_pos = move[0], move[1]

    position = updatepos(position, st_pos, end_pos, colour, piece)

    return position, False
