import numpy as np
from init import CAVES, ACTION_REGISTRY

# ============================================================================
# CAVE EXPLORATION BENEFITS DEFINITION
# ============================================================================
# Each cave has up to 5 benefits that are triggered left-to-right
# Benefit 2 and 4 are the same across all caves:
#   - Benefit 2 (index 1): gain_dragon_guild
#   - Benefit 4 (index 3): lay_egg

CAVE_BENEFITS = {
    1: [  # Crimson Cave
        'gain_any_resource',
        'gain_dragon_guild',      # Common benefit 2
        'gain_any_resource',
        'lay_egg',                # Common benefit 4
        'cache_any_resource_from_hand',
    ],
    2: [  # Golden Grotto
        'gain_dragon_card',
        'gain_dragon_guild',      # Common benefit 2
        'gain_dragon_card',
        'lay_egg',                # Common benefit 4
        'tuck_any_dragon_from_hand',
    ],
    3: [  # Crystal Cavern
        'gain_cave_card',
        'gain_dragon_guild',      # Common benefit 2
        'gain_cave_card',
        'lay_egg',                # Common benefit 4
        'discard_cave_card_from_hand_lay_2_eggs',
    ],
}

# ============================================================================
# CAVE EXPLORATION LOGIC
# ============================================================================

def Explore(game_state, player_hand, player_mat, explore_row):
    """
    Handle cave exploration for a given row (cave).
    
    Parameters:
    -----------
    player_hand : dict
        Player's hand containing resources and cards
    player_mat : dict
        Player's mat with dragons and excavated caves
    explore_row : int
        The cave row to explore (1, 2, or 3)
    
    Returns:
    --------
    None
    """
    if explore_row == 1:
        """Explore the Crimson Cave (Row 1)"""
        activate_cave_benefits(game_state, 1, player_hand, player_mat)
    elif explore_row == 2:
        """Explore the Golden Grotto (Row 2)"""
        activate_cave_benefits(game_state, 2, player_hand, player_mat)
    elif explore_row == 3:
        """Explore the Crystal Cavern (Row 3)"""
        activate_cave_benefits(game_state, 3, player_hand, player_mat)
    else:
        print("Unexpected value for explore row")
    return

def activate_cave_benefits(game_state, cave_id, player_hand, player_mat):
    """
    Activate the benefits of exploring a cave.
    
    The first benefit is free. Each subsequent benefit requires one dragon.
    If a player has 2 dragons in the row, they can activate 3 benefits total
    (1 free + 2 from dragons).
    
    Parameters:
    -----------
    cave_id : int
        The cave ID (1, 2, or 3)
    player_hand : dict
        Player's hand containing resources and cards
    player_mat : dict
        Player's mat with dragons
    
    Returns:
    --------
    None
    """
    # Count dragons in the cave row (0-indexed)
    cave_row_index = cave_id - 1
    dragons_in_row = sum(1 for dragon in player_mat['dragons'][cave_row_index] if dragon != 0)
    
    # Determine how many benefits to activate
    # First benefit is free, then one per dragon
    num_benefits_to_activate = 1 + dragons_in_row
    
    # Get the benefits for this cave
    cave_benefits = CAVE_BENEFITS[cave_id]
    
    # Activate benefits from left to right (within the limit)
    for benefit_index in range(min(num_benefits_to_activate, len(cave_benefits))):
        benefit_name = cave_benefits[benefit_index]
        print(f"Activating benefit {benefit_index + 1}: {benefit_name}")
        
        # Get the action function from the ACTION_REGISTRY
        if benefit_name in ACTION_REGISTRY:
            action_func = ACTION_REGISTRY[benefit_name]
            action_func(game_state, player_hand, player_mat)
        else:
            print(f"Warning: Benefit '{benefit_name}' not found in ACTION_REGISTRY")
    
    return