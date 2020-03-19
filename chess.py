# -*- coding: utf-8 -*-
"""
Trying to build a working chess engine

@author: fmalgarini
"""

from modules.legal_moves import *
from modules.support_func import *
from modules.turns import *
import numpy as np

all_pieces = ['b,r', 'b,k', 'b,b', 'b,q', 'b,K', 'b,p', 'w,r', 'w,k', 'w,b', 'w,q', 'w,K', 'w,p']

def main():
    print("Welcome to TerribleChess! Press q in any moment to quit the game")
    depth, load = read_settings()

    game_over = False

    if load.lower() == 'y':
        game_num = input("Which game would you like to load: ")
        try:
            game_num = int(game_num)
            initial_pos = load_starting_position(game_num)
        except ValueError:
            print("Game not found, sorry")
            initial_pos = initialize_starting_position()
        except Exception as e:
            print(str(e))
            exit()

    else:
        initial_pos = initialize_starting_position()
    pretty_print(initial_pos)
    position = initial_pos

    while not game_over:
        position = player_turn(position)
        pretty_print(position)
        print('\n')
        position = computer_turn(position, depth)
        pretty_print(position)

if __name__ == '__main__':
    main()
