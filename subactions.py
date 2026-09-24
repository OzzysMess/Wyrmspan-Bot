# Handles subactions such as when played abilities, exploring
# a cave, etc.

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

#################################
###### Subaction Functions ######
#################################

# TODO
def activate_OncePerRound_ability(player_hand, player_mat):
    # search for once per round ability in dragon cards
    return

# TODO
def activate_WhenPlayed_ability(player_hand, player_mat):
    # search for when played ability in dragon cards
    return

# TODO
def cache_any_resource_from_gen_supply(player_hand, player_mat):
    # search for when resourcecached ability in dragon cards
    return

# TODO
def cache_any_resource_from_hand(player_hand, player_mat):
    # search for when resourcecached ability in dragon cards
    return

# TODO
def entice_discounted_dragon(player_hand, player_mat):
    return

def discard_cave_card_from_hand_lay_2_eggs(player_hand, player_mat):
    print("Choose a cave card to discard from your hand for 2 eggs:")

    human_discard_cave(player_hand)
    lay_egg(player_hand, player_mat)
    lay_egg(player_hand, player_mat)

    return

def gain_any_resource(player_hand, player_mat):
    print("Choose a resource to gain:")
    print("1. Crystal")
    print("2. Gold")
    print("3. Meat")
    print("4. Milk")
    choice = input("Enter the number of the resource you want to gain: ")
    if choice == "1":
        gain_crystal(player_hand, player_mat)
    elif choice == "2":
        gain_gold(player_hand, player_mat)
    elif choice == "3":
        gain_meat(player_hand, player_mat)
    elif choice == "4":
        gain_milk(player_hand, player_mat)
    else:
        print("Invalid choice, no resource gained.")
    return

def gain_benefit(player_hand, player_mat, benefits):
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

            benefit_handler(player_hand, player_mat)
            return
        print("Invalid choice.")

# TODO
def gain_cave_card(player_hand, player_mat):
    return

def gain_coin(player_hand, player_mat):
    player_hand["coins"] += 1
    return

def gain_crystal(player_hand, player_mat):
    player_hand["resources"]["crystal"] += 1
    return

# TODO
def gain_dragon_card(player_hand, player_mat):
    return

# TODO

def gain_dragon_guild(player_hand, player_mat):
    global guildtrack

    return

def gain_gold(player_hand, player_mat):
    player_hand["resources"]["gold"] += 1
    return

def gain_meat(player_hand, player_mat):
    player_hand["resources"]["meat"] += 1
    return

def gain_milk(player_hand, player_mat):
    player_hand["resources"]["milk"] += 1
    return

def lay_egg(player_hand, player_mat):
    # TODO Implement egg-laying logic, including checking for max eggs and updating player mat
    player_hand["eggs"] += 1
    print("Gained Egg")
    return

# TODO
def offer_to_pay_and_play_cave_card(player_hand, player_mat):
    
    return

def offer_3x(player_hand, player_mat, cost, buys):
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

            benefit_handler(player_hand, player_mat)

# TODO
def swap_dragon_locations(player_hand, player_mat):
    return

# TODO
def tuck_dragon_card_from_deck(player_hand, player_mat):
    return

# TODO
def tuck_any_dragon_from_hand(player_hand, player_mat):
    # search for when resourcecached ability in dragon cards
    return