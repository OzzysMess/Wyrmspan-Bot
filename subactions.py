# Handles subactions such as when played abilities, exploring
# a cave, etc.
import random

######## Helper Functions for subactions ########
# May have to move to a seperate 'interactions' module

def human_discard_cave(player_hand):
    '''Prompt the human player to discard a cave card from their hand'''
    hand_cave_ids = player_hand["hand_caves"]

    if not hand_cave_ids:
        print("No cave cards available.")
        return False

    print(f"Discard one of your cave cards: {hand_cave_ids}")
    
    while True:
        try:
            choice = int(input("Choose a cave card ID to discard: "))
            if choice in hand_cave_ids:
                # Discard card
                player_hand["hand_caves"].remove(choice)
                return True
            else:
                print(f"Invalid choice. Must be one of: {hand_cave_ids}")
        except ValueError:
            print("Please enter a valid integer.")
            continue

def human_discard_dragon(player_hand):
    '''Prompt the human player to discard a dragon card from their hand'''
    hand_dragon_ids = player_hand["hand_dragons"]

    if not hand_dragon_ids:
        print("No dragon cards available.")
        return False

    print(f"Choose a dragon card to discard: {hand_dragon_ids}")

    while True:
        try:
            choice = int(input("Choose a dragon card ID to discard: "))
            if choice in hand_dragon_ids:
                player_hand["hand_dragons"].remove(choice)
                return True
        except ValueError:
            print("Please enter a valid card ID.")
            continue

def human_discard_resource(player_hand):
    '''Prompt the human player to discard a resource from their hand'''

    resources = player_hand["resources"]
    available = [name for name, amount in resources.items() if amount > 0]

    if not available:
        print("You do not have a resource to pay.")
        return False

    print("Choose a resource to discard:")
    for index, resource in enumerate(available, start=1):
        print(f"{index}. {resource}")

    while True:
        try:
            choice = int(input("Resource number: ")) - 1
        except ValueError:
            print("Please enter a valid number.")
            continue
        # Check if the choice is valid
        if 0 <= choice < len(available):
            player_hand["resources"][available[choice]] -= 1
            return True

        print("Invalid choice.")



def pay_offer_cost(player_hand, cost):
    """Pay one offer cost and return whether payment succeeded."""

    if cost == "egg":
        if player_hand["eggs"] < 1:
            print("You do not have an egg to pay.")
            return False

        player_hand["eggs"] -= 1
        return True

    if cost == "dragon_card":
        return human_discard_dragon(player_hand)

    if cost == "cave_card":
        return human_discard_cave(player_hand)

    if cost == "any_resource":
        return human_discard_resource(player_hand)

    print(f"Unsupported offer cost: {cost}")
    return False

def human_choose_showcase_card(game_state, player_hand, card_type):
    """Choose a dragon or cave from the showcase, drawing if that row is empty."""
    card_settings = {
        "dragon": ("dragons", "dragon_deck_ids", "hand_dragons", "dragon"),
        "caves": ("caves", "cave_deck_ids", "hand_caves", "cave"),
    }
    if card_type not in card_settings:
        raise ValueError("card_type must be 'dragon' or 'caves'")

    showcase_key, deck_attribute, hand_key, card_label = card_settings[card_type]
    showcase = game_state.showcase[showcase_key]
    deck = getattr(game_state, deck_attribute)

    if not showcase:
        if not deck:
            print(f"No {card_label} cards remain in the showcase or deck.")
            return None

        card_id = random.choice(deck)
        deck.remove(card_id)
        print(f"The {card_label} showcase is empty; drew card {card_id} from the deck.")
    else:
        print(f"Available {card_label} cards: {showcase}")
        while True:
            try:
                card_id = int(input(f"Choose a {card_label} card ID: "))
            except ValueError:
                print("Please enter a valid card ID.")
                continue

            if card_id not in showcase:
                print(f"Invalid choice. Choose one of: {showcase}")
                continue

            showcase.remove(card_id)
            break
    # TODO: Add card to player hand or leave to calling function to handle?
    player_hand[hand_key].append(card_id)
    return card_id


#################################
###### Subaction Functions ######
#################################

# TODO
def activate_OncePerRound_ability(game_state, player_hand, player_mat):
    # search for once per round ability in dragon cards
    return

# TODO
def activate_WhenPlayed_ability(game_state, player_hand, player_mat):
    # search for when played ability in dragon cards
    return

# TODO
def cache_any_resource_from_gen_supply(game_state, player_hand, player_mat):
    # search for when resourcecached ability in dragon cards
    return

# TODO
def cache_any_resource_from_hand(game_state, player_hand, player_mat):
    # search for when resourcecached ability in dragon cards
    return

# TODO
def entice_discounted_dragon(game_state, player_hand, player_mat):
    return

def discard_cave_card_from_hand_lay_2_eggs(game_state, player_hand, player_mat):
    print("Choose a cave card to discard from your hand for 2 eggs:")

    human_discard_cave(player_hand)
    lay_egg(game_state, player_hand, player_mat)
    lay_egg(game_state, player_hand, player_mat)

    return

def gain_any_resource(game_state, player_hand, player_mat):
    print("Choose a resource to gain:")
    print("1. Crystal")
    print("2. Gold")
    print("3. Meat")
    print("4. Milk")
    choice = input("Enter the number of the resource you want to gain: ")
    if choice == "1":
        gain_crystal(game_state, player_hand, player_mat)
    elif choice == "2":
        gain_gold(game_state, player_hand, player_mat)
    elif choice == "3":
        gain_meat(game_state, player_hand, player_mat)
    elif choice == "4":
        gain_milk(game_state, player_hand, player_mat)
    else:
        print("Invalid choice, no resource gained.")
    return

def gain_benefit(game_state, player_hand, player_mat, benefits):
    """Let the player choose one benefit from a cave card."""

    from init import ACTION_REGISTRY

    print("Choose a benefit to gain:")
    for index, benefit in enumerate(benefits, start=1):
        print(f"{index}. {benefit}")

    while True:
        choice = input(f"Enter the number of the benefit you want to gain (1-{len(benefits)}):")

        try:
            benefit_index = int(choice) - 1
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        if 0 <= benefit_index < len(benefits):
            benefit_name = benefits[benefit_index]
            benefit_handler = ACTION_REGISTRY.get(benefit_name)

            if benefit_handler is None:
                print(f"Warning: Benefit '{benefit_name}' is not implemented.")
                return

            benefit_handler(game_state, player_hand, player_mat)
            return
        print("Invalid choice.")

# TODO
def gain_cave_card(game_state, player_hand, player_mat):
    return

def gain_coin(game_state, player_hand, player_mat):
    player_hand["coins"] += 1
    return

def gain_crystal(game_state, player_hand, player_mat):
    player_hand["resources"]["crystal"] += 1
    return

# TODO
def gain_dragon_card(game_state, player_hand, player_mat):
    return

# TODO
def gain_dragon_guild(game_state, player_hand, player_mat):
    return

def gain_gold(game_state, player_hand, player_mat):
    player_hand["resources"]["gold"] += 1
    return

def gain_meat(game_state, player_hand, player_mat):
    player_hand["resources"]["meat"] += 1
    return

def gain_milk(game_state, player_hand, player_mat):
    player_hand["resources"]["milk"] += 1
    return

def immediately_play_deck_cave_card(game_state, player_hand, player_mat):
    """Draw a cave from the deck and excavate it without normal costs."""
    if not game_state.cave_deck_ids:
        print("No cave cards remain in the deck.")
        return None

    cave_card_id = random.choice(game_state.cave_deck_ids)
    game_state.cave_deck_ids.remove(cave_card_id)

    from excavate import Excavate
    Excavate(game_state, player_hand, player_mat, cave_card_id=cave_card_id)
   

    return cave_card_id

def immediately_play_display_cave_card(game_state, player_hand, player_mat):
    # TODO Implement logic to immediately play a cave card from the display
    return

def lay_egg(game_state, player_hand, player_mat):
    # TODO Implement egg-laying logic, including checking for max eggs and updating player mat
    player_hand["eggs"] += 1
    print("Gained Egg")
    return

def offer_to_pay_and_play_cave_card(game_state, player_hand, player_mat, cost, buys):
    """Pay the two-card/resource cost, then trigger the supported cave action."""
    if len(cost) != 2 or len(buys) != 1:
        print(f"Something is wrong with the cave offer: cost={cost}, buys={buys}")
        return False

    from init import ACTION_REGISTRY

    action_handler = ACTION_REGISTRY.get(buys[0])
    if action_handler is None:
        print(f"Unsupported cave offer action: {buys[0]}")
        return False

    if not game_state.cave_deck_ids:
        print("No cave cards remain in the deck.")
        return False

    answer = input("Pay the cost and play a cave from the deck? (Y/n): ").strip().lower()
    if answer not in {"", "y", "yes", "ye", "ys"}:
        return False

    cost_type = cost[0]
    if cost_type == "egg":
        can_pay = player_hand["eggs"] >= 2
    elif cost_type == "dragon_card":
        can_pay = len(player_hand["hand_dragons"]) >= 2
    elif cost_type == "cave_card":
        can_pay = len(player_hand["hand_caves"]) >= 2
    elif cost_type == "any_resource":
        can_pay = sum(player_hand["resources"].values()) >= 2
    else:
        print(f"Unsupported cave offer cost: {cost_type}")
        return False

    if not can_pay:
        print(f"You cannot pay the cost: {cost}")
        return False

    for _ in cost:
        if not pay_offer_cost(player_hand, cost_type):
            return False

    action_handler(game_state, player_hand, player_mat)
    return True

def offer_3x(game_state, player_hand, player_mat, cost, buys):
    """Allow the player to pay the cost up to three times."""

    cost = cost[0] if isinstance(cost, list) else cost

    for offer_number in range(1, 4):
        answer = input(
            f"Accept offer {offer_number}/3 and pay {cost}? (Y/n): "
        ).strip().lower()
        # End if not a yes
        if answer not in {"", "y", "yes", "ye", "ys"}:
            break
        # Stop if the player cannot pay the cost
        if not pay_offer_cost(player_hand, cost):
            break

        from init import ACTION_REGISTRY

        for buy in buys:
            benefit_handler = ACTION_REGISTRY.get(buy)

            if benefit_handler is None:
                print(f"Unsupported benefit: {buy}")
                continue

            benefit_handler(game_state, player_hand, player_mat)

# TODO
def swap_dragon_locations(game_state, player_hand, player_mat):
    return

# TODO
def tuck_dragon_card_from_deck(game_state, player_hand, player_mat):
    return

# TODO
def tuck_any_dragon_from_hand(game_state, player_hand, player_mat):
    # search for when resourcecached ability in dragon cards
    return