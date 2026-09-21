import json
import pandas as pd
from pathlib import Path
import random
import subactions

# ============================================================================
# GLOBAL GAME CONFIGURATION - Available to all modules
# ============================================================================

# Load cave cards database
script_dir = Path(__file__).parent
data_dir = script_dir / "wyrm-data"

with open(data_dir / "CAVES.json", 'r') as f:
    CAVES_LIST = json.load(f)

# Convert to dictionary for fast lookup by ID
CAVES = {cave['id']: cave for cave in CAVES_LIST}

# Action registry mapping action names to subactions functions
# This is used by excavate.py and other modules to execute cave card abilities
ACTION_REGISTRY = {
    'activate_OncePerRound_ability': subactions.activate_OncePerRound_ability,
    'cache_any_resource_from_gen_supply': subactions.cache_any_resource_from_gen_supply,
    'gain_any_resource': subactions.gain_any_resource,
    'gain_cave_card': subactions.gain_cave_card,
    'gain_coin': subactions.gain_coin,
    'gain_crystal': subactions.gain_crystal,
    'gain_dragon_card': subactions.gain_dragon_card,
    'gain_dragon_guild': subactions.gain_dragon_guild,
    'gain_gold': subactions.gain_gold,
    'gain_meat': subactions.gain_meat,
    'gain_milk': subactions.gain_milk,
    'lay_egg': subactions.lay_egg,
    'swap_dragon_locations': subactions.swap_dragon_locations,
    'tuck_dragon_card_from_deck': subactions.tuck_dragon_card_from_deck,
}

# ============================================================================

def initialize_game():
    dragons, caves, dragon_deck_ids, cave_deck_ids = initialize_deck()
    showcase, dragon_deck_ids, cave_deck_ids = initialize_showcase(dragon_deck_ids, cave_deck_ids)
    # Default is human choices, use second line for random
    # player1_hand, dragon_deck_ids, cave_deck_ids = initialize_player_hand("Obama", dragon_deck_ids, cave_deck_ids, human_choose_dragon, human_choose_cave, human_choose_resources)
    
    player1_hand, dragon_deck_ids, cave_deck_ids = initialize_player_hand(
         "Obama", dragon_deck_ids, cave_deck_ids, None,
           None, _random_starting_resources)
    
    player1_mat = initialize_player_mat()
    guildtrack = initialize_guildtrack()
    return dragons, caves, showcase, guildtrack, player1_hand, player1_mat, dragon_deck_ids, cave_deck_ids

def initialize_deck(dragon_ids=None, cave_ids=None):
    """
    Initialize the deck by loading dragon and cave cards from JSON files.
    
    Parameters:
    -----------
    dragon_ids : list or range, optional
        List of dragon card IDs to load. Defaults to range(1, 181) for IDs 1-180.
    cave_ids : list or range, optional
        List of cave card IDs to load. Defaults to range(1, 81) for IDs 1-80.
    
    Returns:
    --------
    tuple : (dragons_df, caves_df)
        DataFrames containing loaded dragon and cave cards.
    """
    
    # Set defaults if not provided
    if dragon_ids is None:
        dragon_ids = list(range(1, 184))  # 1-183
    else:
        dragon_ids = list(dragon_ids)
    
    if cave_ids is None:
        cave_ids = list(range(1, 76))  # 1-75
    else:
        cave_ids = list(cave_ids)
    
    # Get the directory of this script
    script_dir = Path(__file__).parent
    data_dir = script_dir / "wyrm-data"

    # Load dragon cards
    dragons_path = data_dir / "dragons-with-abilities.json"
    with open(dragons_path, 'r') as f:
        dragons_data = json.load(f)
    
    # Load cave cards
    caves_path = data_dir / "CAVES.json"
    with open(caves_path, 'r') as f:
        caves_data = json.load(f)
    
    # Convert to DataFrames
    dragons_df = pd.DataFrame(dragons_data)
    caves_df = pd.DataFrame(caves_data)
    
    # Convert ID columns to integers for proper comparison
    dragons_df['id'] = dragons_df['id'].astype(int)
    caves_df['id'] = caves_df['id'].astype(int)
    
    # Filter by requested IDs
    dragons_deck = dragons_df[dragons_df['id'].isin(dragon_ids)].reset_index(drop=True)
    caves_deck = caves_df[caves_df['id'].isin(cave_ids)].reset_index(drop=True)
    
    return dragons_deck, caves_deck, dragon_ids, cave_ids

def initialize_showcase(dragon_deck_ids, cave_deck_ids):
    """
    Initialize the showcase by randomly selecting 3 dragon and 3 cave cards.
    
    Parameters:
    -----------
    dragon_deck_ids : list
        List of dragon card IDs available in the deck.
    cave_deck_ids : list
        List of cave card IDs available in the deck.
    
    Returns:
    --------
    showcase : dict
        Dictionary with 'dragons' and 'caves' keys containing selected IDs.
    new_dragon_deck_ids : list
        Updated dragon IDs excluding showcase cards.
    new_cave_deck_ids : list
        Updated cave IDs excluding showcase cards.
    """
    
    # Safely handle cases where there are fewer than 3 cards
    # num_dragons = min(3, len(dragon_deck_ids))
    # num_caves = min(3, len(cave_deck_ids))
    
    # Randomly select cards for showcase
    showcase_dragons = random.sample(dragon_deck_ids, 3)
    showcase_caves = random.sample(cave_deck_ids, 3)
    
    # Create showcase dict
    showcase = {
        'dragons': showcase_dragons,
        'caves': showcase_caves
    }
    
    # Create new deck IDs excluding showcase cards
    new_dragon_deck_ids = [id for id in dragon_deck_ids if id not in showcase_dragons]
    new_cave_deck_ids = [id for id in cave_deck_ids if id not in showcase_caves]
    
    return showcase, new_dragon_deck_ids, new_cave_deck_ids

def initialize_player_hand(
    name,
    dragon_deck_ids,
    cave_deck_ids,
    choose_dragon_fn=None,
    choose_cave_fn=None,
    choose_resources_fn=None
):
    """
    Initialize a player with starting hand and resources.
    
    Parameters:
    -----------
    name : str
        Player name.
    dragon_deck_ids : list
        List of available dragon card IDs in the deck. Will draw 3 randomly.
    cave_deck_ids : list
        List of available cave card IDs in the deck. Will draw 3 randomly.
    choose_cave_fn : callable, optional
        Function to choose which cave to discard: (hand_caves) -> cave_id.
        Defaults to random selection.
    choose_dragon_fn : callable, optional
        Function to choose which dragon to discard: (hand_dragons) -> dragon_id.
        Defaults to random selection.
    choose_resources_fn : callable, optional
        Function to choose starting resources: () -> dict with keys 'milk', 'crystal', 'gold', 'meat'.
        Defaults to random selection.
    
    Returns:
    --------
    tuple : (player, remaining_dragon_ids, remaining_cave_ids)
        player : dict
            Dictionary containing player state:
            - name: player name
            - coins: starting coins (6)
            - hand_caves: cave card IDs after discard (2)
            - hand_dragons: dragon card IDs after discard (2)
            - eggs: starting eggs (2)
            - resources: dict with resource counts
        remaining_dragon_ids : list
            Updated dragon deck IDs after drawing 3 cards.
        remaining_cave_ids : list
            Updated cave deck IDs after drawing 3 cards.
    """
    
    # Draw 3 random cards from each deck
    drawn_dragons = random.sample(dragon_deck_ids, 3)
    drawn_caves = random.sample(cave_deck_ids, 3)
    print(f"Your dragons cards: {drawn_dragons}")
    print(f"Your cave cards: {drawn_caves}")
    # Remove drawn cards from deck
    remaining_dragon_ids = [id for id in dragon_deck_ids if id not in drawn_dragons]
    remaining_cave_ids = [id for id in cave_deck_ids if id not in drawn_caves]
    
    # Set default decision functions to random selection
    if choose_cave_fn is None:
        choose_cave_fn = lambda caves: random.choice(caves)
    
    if choose_dragon_fn is None:
        choose_dragon_fn = lambda dragons: random.choice(dragons)
    
    if choose_resources_fn is None:
        # Random: select 3 resources from 4 types
        choose_resources_fn = lambda: _random_starting_resources()
    
    # Player chooses which dragon to discard from hand
    dragon_to_discard = choose_dragon_fn(drawn_dragons)
    hand_dragons = [d for d in drawn_dragons if d != dragon_to_discard]
    
    # Player chooses which cave to discard from hand
    cave_to_discard = choose_cave_fn(drawn_caves)
    hand_caves = [c for c in drawn_caves if c != cave_to_discard]
    
    # Player chooses starting resources
    resources = choose_resources_fn()
    
    # Create player dict
    player = {
        'name': name,
        'coins': 6,
        'hand_caves': [hand_caves],
        'hand_dragons': [hand_dragons],
        'eggs': 2,
        'resources': resources,
        'guild_position': 0
    }
    print(f"Your dragon cards: {hand_dragons}")
    print(f"Your cave cards: {hand_caves}")
    return player, remaining_dragon_ids, remaining_cave_ids

def initialize_guildtrack():
    """
    
    TODO: Guilds

    Initialize the guild board with the guildtrack and player position tracking.
    
    The guildtrack contains 12 different triggers/actions that occur when a player
    advances to each position on the track. Player position starts at 0 but does not
    trigger the action at spot 0 until lapping during gameplay.
    
    Returns:
    --------
    guild_board : dict
        Dictionary containing:
        - 'guildtrack': List of 12 action descriptors (0-11)
    """
    guildtrack = [
        "Gain 1 VP",              # 0
        "Gain 1 Egg",             # 1
        "Gain 1 Meat",            # 2
        "Gain 1 DragonCard",      # 3
        "Gain 1 CaveCard",        # 4
        "Gain 1 Crystal",         # 5
        "Gain 1 VP",              # 6
        "Gain 1 Egg",             # 7
        "Gain 1 Gold",            # 8
        "Gain 1 DragonCard",      # 9
        "Gain 1 Coin",            # 10
        "Gain 1 Milk"             # 11
    ]
    
    return guildtrack

def _random_starting_resources():
    """
    Generate random starting resources (3 total from milk, crystal, gold, meat).
    
    Returns:
    --------
    resources : dict
        Dictionary with resource counts summing to 3.
    """
    resource_types = ['milk', 'crystal', 'gold', 'meat']
    selected_resources = random.choices(resource_types, k=3)
    
    resources = {
        'milk': selected_resources.count('milk'),
        'crystal': selected_resources.count('crystal'),
        'gold': selected_resources.count('gold'),
        'meat': selected_resources.count('meat')
    }
    print(f"\nRandomly assigned starting resources: {resources}")
    return resources


def human_choose_cave(hand_cave_ids):
    """
    Interactive function for human player to choose a cave card to discard.
    
    Parameters:
    -----------
    hand_cave_ids : list
        Cave card IDs in player's hand.
    
    Returns:
    --------
    cave_id : int
        The cave card ID chosen to discard.
    """
    print(f"Discard one of your cave cards: {hand_cave_ids}")
    
    while True:
        try:
            choice = int(input("Choose a cave card ID to discard: "))
            if choice in hand_cave_ids:
                return choice
            else:
                print(f"Invalid choice. Must be one of: {hand_cave_ids}")
        except ValueError:
            print("Please enter a valid integer.")


def human_choose_dragon(hand_dragon_ids):
    """
    Interactive function for human player to choose a dragon card to discard.
    
    Parameters:
    -----------
    hand_dragon_ids : list
        Dragon card IDs in player's hand.
    
    Returns:
    --------
    dragon_id : int
        The dragon card ID chosen to discard.
    """
    print(f"Discard one of your dragon cards: {hand_dragon_ids}")
    
    while True:
        try:
            choice = int(input("Choose a dragon card ID to discard: "))
            if choice in hand_dragon_ids:
                return choice
            else:
                print(f"Invalid choice. Must be one of: {hand_dragon_ids}")
        except ValueError:
            print("Please enter a valid integer.")
    


def human_choose_resources():
    """
    Interactive function for human player to choose starting resources.
    
    Returns:
    --------
    resources : dict
        Dictionary with resource counts summing to 3.
    """
    resource_types = ['milk', 'crystal', 'gold', 'meat']
    resources = {rt: 0 for rt in resource_types}
    
    print("Choose 3 resources total (milk, crystal, gold, meat)")
    remaining = 3
    
    while remaining > 0:
        
        choice = input(f"Choose a resource ({remaining} left): ").lower()
        
        if choice in resource_types:
            resources[choice] += 1
            remaining -= 1
        else:
            print(f"Invalid choice. Must be one of: {resource_types}")
    print(f"\nResources chosen: {resources}")
    return resources


def initialize_player_mat():
    """
    Initialize a player's mat (3x4 grid for dragon placement and excavation).
    
    Structure:
    - dragons: 3x4 grid. 0 = empty space, positive int = dragon ID
    - excavated: 3x3 grid for columns 2-4 (column 1 is always excavated)
      0 = unexcavated space, positive int = cave card ID that excavated it
    - egg_costs: Cost in eggs to excavate each column [col2, col3, col4] = [0, 1, 2]
    
    Returns:
    --------
    mat : dict
        Dictionary containing:
        - 'dragons': 3x4 list of lists (dragon IDs or 0)
        - 'excavated': 3x3 list of lists (cave IDs or 0 for columns 2-4)
        - 'egg_costs': [0, 1, 2] for egg costs of columns 2, 3, 4
    """
    mat = {
        'dragons': [[0]*4 for _ in range(3)],  # 3x4 grid, all empty initially
        'excavated': [[0]*3 for _ in range(3)],  # 3x3 grid for columns 2-4, all unexcavated
    }
    return mat


# might delete or move the cave functions below
def place_dragon_on_mat(mat, dragon_id, row, col):
    """
    Place a dragon on the player's mat.
    
    Parameters:
    -----------
    mat : dict
        Player's mat dictionary.
    dragon_id : int
        ID of the dragon to place.
    row : int
        Row position (0-2).
    col : int
        Column position (0-3).
    
    Returns:
    --------
    bool : True if placement successful, False if space occupied or invalid position.
    """
    if row < 0 or row >= 3 or col < 0 or col >= 4:
        return False
    
    if mat['dragons'][row][col] == 0:
        mat['dragons'][row][col] = dragon_id
        return True
    
    return False


def excavate_space(mat, cave_card_id, row, col):
    """
    Excavate a space on the player's mat.
    
    Parameters:
    -----------
    mat : dict
        Player's mat dictionary.
    cave_card_id : int
        ID of the cave card used to excavate.
    row : int
        Row position (0-2).
    col : int
        Column position (1-3, column 1 is already excavated).
    
    Returns:
    --------
    bool : True if excavation successful, False if invalid or already excavated.
    """
    if row < 0 or row >= 3 or col < 1 or col >= 4:
        return False
    
    excavated_col_idx = col - 1  # Convert to excavated array index (0-2)
    
    if mat['excavated'][row][excavated_col_idx] == 0:
        mat['excavated'][row][excavated_col_idx] = cave_card_id
        return True
    
    return False


def is_space_excavated(mat, row, col):
    """
    Check if a space is excavated.
    
    Parameters:
    -----------
    mat : dict
        Player's mat dictionary.
    row : int
        Row position (0-2).
    col : int
        Column position (0-3).
    
    Returns:
    --------
    bool : True if space is excavated (or column 1), False otherwise.
    """
    if row < 0 or row >= 3 or col < 0 or col >= 4:
        return False
    
    # Column 0 is always excavated
    if col == 0:
        return True
    
    excavated_col_idx = col - 1
    return mat['excavated'][row][excavated_col_idx] != 0


def can_place_dragon(mat, row, col):
    """
    Check if a dragon can be placed at a position (space must be excavated and empty).
    
    Parameters:
    -----------
    mat : dict
        Player's mat dictionary.
    row : int
        Row position (0-2).
    col : int
        Column position (0-3).
    
    Returns:
    --------
    bool : True if dragon can be placed, False otherwise.
    """
    if row < 0 or row >= 3 or col < 0 or col >= 4:
        return False
    
    return is_space_excavated(mat, row, col) and mat['dragons'][row][col] == 0