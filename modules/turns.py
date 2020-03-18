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
              valid_input = False
              st_pos = input("Insert the coordinates of the piece you want to move: ").split(',')
              if st_pos[0] == 's':
                  print("Saving position... ")
                  save_position(position)
                  print("Quitting program")
                  exit()
              elif st_pos[0] == 'q':
                  sure = input("Quitting without saving. Are you sure? (Y/N): ")
                  if sure.lower() == 'y':
                      exit()

              while len(st_pos) != 2:
                  st_pos = input("You must insert two coordinates, separated by a comma: ").split(',')
              while not valid_input:
                  try:
                      st_pos = list(map(int, st_pos))
                      valid_input = True

                  except ValueError:
                      st_pos = input("The coordinates must be integer values, not characters: ").split(',')

                  except Exception as e:
                      print(str(e))
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
              valid_input = False
              while not valid_input:
                  try:
                      end_pos = list(map(int, end_pos))
                      valid_input = True

                  except ValueError:
                      end_pos = input("The coordinates must be integer values, not characters: ").split(',')

                  except Exception as e:
                      print(str(e))
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
