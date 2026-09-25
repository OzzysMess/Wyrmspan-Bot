import numpy as np
from init import ACTION_REGISTRY

# TODO
# Final column excavation offer for a turn coin

def egg_cost_for_excavation(column):
    '''Cost to excavate column 2, 3, 4 (column 1 is free at 0)
    Column index use game indexing (1-4)''' 
    return np.max([(column - 1),0])

def can_excavate(player_hand, player_mat, free_play=False):
    '''Check cave cards > 0, empty slots, enough eggs'''
    #TODO: option to skip cave cave ability 

    if not free_play and len(player_hand["hand_caves"]) == 0:
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
    if not free_play and player_hand["eggs"] < min_egg_cost:
        print(f"Not enough eggs to excavate!")
        return False

    return True

def Excavate(game_state, player_hand, player_mat, cave_card_id=None):
    '''Perform excavation action
    - Player selects what cave card to excavate with
    - Player selects where on mat to excavate (row, col) 
    - Do excavation check
    - Update player hand and mat
    - Do cave card ability

    If cave_card_id is provided, play that cave for free without requiring it
    to be in the player's hand.'''

    free_play = cave_card_id is not None
    if free_play:
        cave_rows = game_state.caves.loc[game_state.caves["id"] == cave_card_id]

    else:
        print("Available cave cards in hand:")
        print(player_hand["hand_caves"])
        try:
            cave_card_id = int(input("Enter the cave card ID you want to excavate with: "))
        except ValueError:
            print("Enter a valid cave card ID.")
            player_hand["coins"] += 1
            return False

        if cave_card_id not in player_hand["hand_caves"]:
            player_hand["coins"] += 1
            print(f"Cave card {cave_card_id} not found in hand!")
            return False

    
    #Choose where to excavate
    print("Where would like to excavate?)")
    try:
        row = int(input("Enter the cave to excavate row (1-3):"))
    except ValueError:
        print("Enter a valid row number.")
        if not free_play:
            player_hand["coins"] += 1
        return False
    if row not in range(1, 4):
        print("Row must be between 1 and 3.")
        if not free_play:
            player_hand["coins"] += 1
        return False
    # column would be the first column that is not excavated in
    # the player_mat for a given row
    # +2 to convert to game column index
    row_slots = player_mat['excavated'][row - 1]
    if 0 not in row_slots:
        print(f"Row {row} has no unexcavated slots.")
        if not free_play:
            player_hand["coins"] += 1
        return False
    column = row_slots.index(0) + 2

    slot = np.array([int(row), column])

    if not can_excavate(player_hand, player_mat, free_play=free_play):
        print("Cannot excavate!")
        if not free_play:
            player_hand["coins"] += 1  # refund the coin
        return False

    egg_cost = 0 if free_play else egg_cost_for_excavation(slot[1])
    player_hand["eggs"] -= egg_cost
    # Update player_mat to mark the column as excavated
    # Recall excavated array is 3x3 for columsns 2-4
    player_mat['excavated'][slot[0]-1][slot[1]-2] = 1  # Mark as excavated
    print(f"Excavated {slot} for {egg_cost} eggs!")

    do_cave_card_ability(game_state, cave_card_id, player_hand, player_mat)
    # Remove the cave card from the player's hand
    try:
        player_hand["hand_caves"].remove(cave_card_id)
    except:
        print(f"Warning: Cave card {cave_card_id} not found in hand during removal.")

    # Special action if last column in a row is dug out
    if slot[1] == 4:
        print(f"Last column in row {slot[0]} excavated! You may trade in 3 items for a coin.")
        do_special_trade_in(game_state, player_hand, player_mat)

    return True

def do_cave_card_ability(game_state, cave_card_ID, player_hand, player_mat):
    '''Perform the ability of the excavated cave card'''
    cave_rows = game_state.caves.loc[game_state.caves["id"] == cave_card_ID]
    if cave_rows.empty:
        print(f"Cave card {cave_card_ID} not found!")
        return
    
    cave_card = cave_rows.iloc[0]
    
    # Execute each action in sequence
    for action_name in cave_card["actions"]:
        if action_name not in ACTION_REGISTRY:
            print(f"Warning: Action '{action_name}' not found in ACTION_REGISTRY")
            continue

        action_handler = ACTION_REGISTRY[action_name]

        if action_name == "gain_benefit":
            action_handler(
                game_state,
                player_hand,
                player_mat,
                cave_card.get("benefits", [])
            )
        elif action_name == "offer_3x":
            action_handler(
            game_state,
            player_hand,
            player_mat,
            cave_card.get("cost", []),
            cave_card.get("buys", [])
            )
        elif action_name == "offer_to_pay_and_play_cave_card":
            action_handler(
                game_state,
                player_hand,
                player_mat,
                cave_card.get("cost", []),
                cave_card.get("buys", []),
            )
        else:
            action_handler(game_state, player_hand, player_mat)
    return

def do_special_trade_in(game_state, player_hand, player_mat):
    '''Trade in 3 items for a coin: resources or cards'''
    return True