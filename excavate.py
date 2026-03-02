import numpy as np

def egg_cost_for_excavation(column):
    '''Cost to excavate column 2, 3, 4 (column 1 is free at 0)''' 
    return np.max([(column - 1),0])

def can_excavate():
    '''Check cave cards > 0, empty slots, enough eggs'''
    return True

def Excavate(player_hand, player_mat, column):
    '''Perform excavation action
    - Player selects what cave card to excavate with
    - Player selects where on mat to excavate (row, col) 
    - Do excavation check
    - Update player hand and mat
    - Do cave card ability'''
    if not can_excavate():
        print("Cannot excavate!")
        player_hand["coins"] += 1  # refund the coin
    
    cost = egg_cost_for_excavation(column)
    player_hand["eggs"] -= cost
    # Update player_mat to mark the column as excavated
    player_mat['excavated'][column-1] = 1  # Mark as excavated
    print(f"Excavated column {column} for {cost} eggs!")