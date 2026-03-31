import numpy as np
from init import CAVES, ACTION_REGISTRY

def Explore(player_hand, player_mat, explore_row):
    exploring_dragons = player_mat['dragons'][explore_row-1]
    if explore_row == 1:
        explore_crimson_cave(player_hand, player_mat)
    elif explore_row == 2:
        explore_goldern_grotto(player_hand, player_mat)
    elif explore_row == 3:
        explore_crystal_cavern(player_hand, player_mat)
    else:
        print("Unexpected value for explore row")
    return

def explore_crimson_cave(player_hand, player_mat):
    return

def explore_goldern_grotto(player_hand, player_mat):
    return

def explore_crystal_cavern(player_hand, player_mat):
    return