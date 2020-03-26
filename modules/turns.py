# -*- coding: utf-8 -*-
"""
Functions for the turns of player and computer

@author: fmalgarini
"""
from modules.support_func import *

player = {"w":0, "b":1}

def player_turn(position, move_num):

    colour = 0 #For now player can only use white
    if is_in_check(position, colour, move_num):
        print("Check!")

    is_valid = False
    s_castle = False
    l_castle = False

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
              elif st_pos[0].lower() == 'scastle' or st_pos[0].lower() == 'castle':
                  st_pos = [7,4]
                  s_castle = True

              elif st_pos[0].lower() == 'lcastle':
                  st_pos = [7,4]
                  l_castle = True

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
              if not l_castle and not s_castle:
                  end_pos = input("Insert the coordinates of the destination of the piece: ").split(',')
                  valid_input = False
                  while len(end_pos) != 2:
                      end_pos = input("You must insert two coordinates, separated by a comma: ").split(',')
                  while not valid_input:
                      try:
                          end_pos = list(map(int, end_pos))
                          valid_input = True

                      except ValueError:
                          end_pos = input("The coordinates must be integer values, not characters: ").split(',')

                      except Exception as e:
                          print(str(e))
                          exit()
              elif s_castle:
                  end_pos = [7,7]
              else:
                  end_pos = [7,0]

              if check_valid_coord(st_pos, end_pos):
                  break

          is_valid = check_move(piece, position, st_pos, end_pos, colour, 0)

    temp = position.copy()
    if s_castle == True:
        short = True
        position = castle(position, short, colour)
    elif l_castle == True:
        short = False
        position = castle(position, short, colour)
    else:
        position = updatepos(position, st_pos, end_pos, colour, piece)

    while is_in_check(position, colour, move_num):
        print("You are in check! Choose a valid move: ")
        position = player_turn(temp, move_num)

    return position

def computer_turn(position, depth, move_num):

    colour = 1 #For now computer plays with black
    if is_in_check(position, colour, move_num):
        print("Check!")
        move, piece = handle_check(position, colour, move_num)

    else:
        if depth == 1:
            possible_moves = compute_legal_moves(position, colour, 0, move_num)
            move, piece = prepare_move_depth_1(possible_moves, -1)

        elif depth == 2:
            #possible_moves = compute_legal_moves(position, colour, 1, move_num)
            possible_moves = compute_legal_moves(position, colour, 1, move_num)
            move, piece = prepare_move_depth_2(possible_moves, position)

        else:
            print("Warning: depth {0} not implemented yet. Using depth = 2".format(depth))
            possible_moves = compute_legal_moves(position, colour, 1, move_num)
            move, piece = prepare_move_depth_2(possible_moves, position)

    st_pos, end_pos = move[0], move[1]
    #Because of how compute_legal_moves works, at this point the chosen move is certainly valid.
    #Still, it is necessary to call check_move with flag 0 so that the global variable b_king_moved
    #in legal_moves.py can be changed to True when the black king is moved, and the computer can
    #be prevented from illegally castling
    if piece == 'K':
        check_move(piece, position, st_pos, end_pos, colour, 0)

    temp = position.copy()
    position = updatepos(position, st_pos, end_pos, colour, piece)

    #TODO: If an illegal best move is computed that leaves the king in check (when he wasn't before
    #the move), the next two lines will recursively call this function forever.
    #Write code to break this loop (altough it happened when the king was worth 0 points, now that
    #it is worth 100 it's unlikely that the best move point-wise will expose the king to capture)
    if is_in_check(position, colour, move_num):
        computer_turn(temp, depth, move_num)

    return position
