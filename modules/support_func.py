# -*- coding: utf-8 -*-
"""
Support functions for chess engine

@author: fmalgarini
"""

point_dict = {'r':5, 'k':3, 'b':3, 'q':9, 'K':0, 'p':1}

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
