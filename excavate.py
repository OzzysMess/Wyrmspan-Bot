import numpy as np
from init import CAVES, ACTION_REGISTRY 

# TODO
# Final column excavation offer for a turn coin

def egg_cost_for_excavation(column):
    '''Cost to excavate column 2, 3, 4 (column 1 is free at 0)
    Column index use game indexing (1-4)''' 
    return np.max([(column - 1),0])

def can_excavate(player_hand, player_mat):
    '''Check cave cards > 0, empty slots, enough eggs'''
    #TODO: option to skip cave cave ability 

    if len(player_hand["hand_caves"]) == 0:
        print("No cave cards in hand!")
        return False

    # Find the leftmost unexcavated slot anywhere on the player's mat.
    unexcavated_columns = np.argwhere(np.asarray(player_mat['excavated']) == 0)
    if len(unexcavated_columns) == 0:
        print("No unexcavated slots available!")
        return False
    #check if player has enough eggs to excavate the leftmost unexcavated column
    leftmost_unexcavated_column = unexcavated_columns[0][1] + 2  # +2 to convert to game column index
    min_egg_cost = egg_cost_for_excavation(leftmost_unexcavated_column)
    if player_hand["eggs"] < min_egg_cost:
        print(f"Not enough eggs to excavate!")
        return False

    return True

def Excavate(player_hand, player_mat):
    '''Perform excavation action
    - Player selects what cave card to excavate with
    - Player selects where on mat to excavate (row, col) 
    - Do excavation check
    - Update player hand and mat
    - Do cave card ability'''


    #Choose cave card
    print("Availble cave cards in hand:")
    print(player_hand["hand_caves"])
    cave_card_ID = input("Enter the cave card ID you want to excavate with: ") 

    if cave_card_ID not in player_hand["hand_caves"]:
        # wrong cave ID, return coin to player and exit
        player_hand["coins"] += 1
        print(f"Cave card {cave_card_ID} not found in hand!")
        return
        

    
    #Choose where to excavate
    print("Where would like to excavate?)")
    row = int(input("Enter the cave to excavate row (1-3):"))
    if row not in range(1, 4):
        print("Row must be between 1 and 3.")
        player_hand["coins"] += 1
        return
    # column would be the first column that is not excavated in
    # the player_mat for a given row
    # +2 to convert to game column index
    row_slots = player_mat['excavated'][row - 1]
    if 0 not in row_slots:
        print(f"Row {row} has no unexcavated slots.")
        player_hand["coins"] += 1
        return
    column = row_slots.index(0) + 2

    slot = np.array([int(row), column])

    if not can_excavate(player_hand, player_mat):
        print("Cannot excavate!")
        player_hand["coins"] += 1  # refund the coin
        return

    egg_cost = egg_cost_for_excavation(slot[1])
    player_hand["eggs"] -= egg_cost
    # Update player_mat to mark the column as excavated
    # Recall excavated array is 3x3 for columsns 2-4
    player_mat['excavated'][slot[0]-1][slot[1]-2] = 1  # Mark as excavated
    print(f"Excavated {slot} for {egg_cost} eggs!")

    do_cave_card_ability(cave_card_ID, player_hand, player_mat)
    # Remove the cave card from the player's hand
    player_hand["hand_caves"].remove(cave_card_ID)
    
    return

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
            action_handler(player_hand, player_mat)
        else:
            print(f"Warning: Action '{action_name}' not found in ACTION_REGISTRY")
    
    return
