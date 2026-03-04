import numpy as np
from init import CAVES, ACTION_REGISTRY 

def egg_cost_for_excavation(column):
    '''Cost to excavate column 2, 3, 4 (column 1 is free at 0)''' 
    return np.max([(column - 1),0])

def can_excavate():
    '''Check cave cards > 0, empty slots, enough eggs,
     if cave ID =52 check dragons,'''
    return True

def Excavate(player_hand, player_mat, column):
    '''Perform excavation action
    - Player selects what cave card to excavate with
    - Player selects where on mat to excavate (row, col) 
    - Do excavation check
    - Update player hand and mat
    - Do cave card ability'''


    #Choose cave card
    print("Availble cave cards in hand:")
    print(player_hand["cave_cards"])
    cave_card_ID = input("Enter the cave card ID you want to excavate with: ") 
    
    #Choose where to excavate
    print("Where would like to excavate?)")
    row = input("Enter the cave to excavate row (1-3):")
    # column would be the first column that is not excavated in
    # the player_mat for a given row
    # +2 to convert to game column index
    column = np.where(player_mat['excavated'][int(row)-1] == 0)[0][0] + 2  

    slot = np.array([int(row), column])

    if not can_excavate():
        print("Cannot excavate!")
        player_hand["coins"] += 1  # refund the coin
        return

    egg_cost = egg_cost_for_excavation(slot[1])
    player_hand["eggs"] -= egg_cost
    # Update player_mat to mark the column as excavated
    # Recall excavated array is 3x3 for columsns 2-4
    player_mat['excavated'][slot[1]-2] = 1  # Mark as excavated
    print(f"Excavated {slot} for {egg_cost} eggs!")

    do_cave_card_ability(cave_card_ID, player_hand, player_mat)

def do_cave_card_ability(cave_card_ID, player_hand, player_mat):
    '''Perform the ability of the excavated cave card'''
    if cave_card_ID not in CAVES:
        print(f"Cave card {cave_card_ID} not found!")
        return
    
    cave_card = CAVES[cave_card_ID]
    
    # Execute each action in sequence
    for action_name in cave_card["actions"]:
        if action_name in ACTION_REGISTRY:
            action_handler = ACTION_REGISTRY[action_name]
            action_handler(cave_card, player_hand, player_mat)
        else:
            print(f"Warning: Action '{action_name}' not found in ACTION_REGISTRY")
    
    return
