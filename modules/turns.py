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

def computer_turn(position):

    possible_moves = {}

    colour = 1
    all_positions = [(x,y) for x in range(0,8) for y in range(0,8)]
    possible_starting_positions = [(x,y) for x in range(0,8) for y in range(0,8) if position[x][y][0] == 'b']
    for st_pos in possible_starting_positions:
        piece = position[st_pos[0]][st_pos[1]]

        if piece == 'emp':
            break
        for end_pos in all_positions:
            if check_move(piece, position, st_pos, end_pos, colour, 1):

                temp_position = updatepos(position, st_pos, end_pos, colour, piece)

                points_w, points_b = calc_points(temp_position)
                tentative_pos = [st_pos, end_pos, piece]
                possible_moves.update({str(tentative_pos):points_w})
            else:
                continue

    move, piece = prepare_move(possible_moves)
    st_pos, end_pos = move[0], move[1]

    position = updatepos(position, st_pos, end_pos, colour, piece)

    return position, False
