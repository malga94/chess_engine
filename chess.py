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
    depth = read_settings()
    game_over = False

    initial_pos = initialize_starting_position()
    print(initial_pos)
    position = initial_pos

    while not game_over:
        position, game_over = player_turn(position)
        print(position)
        print('\n')
        position, game_over = computer_turn(position, depth)
        print(position)

if __name__ == '__main__':
    main()
