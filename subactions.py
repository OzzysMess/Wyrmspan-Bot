# Handles subactions such as when played abilities, exploring
# a cave, etc.

###### Helper Functions for subactions ######
# May have to move to a seperate 'interactions' module

def human_discard_cave(player_hand):
    '''Prompt the human player to choose a cave card from their hand'''
    hand_cave_ids = player_hand["hand_caves"]
    print(f"Discard one of your cave cards: {hand_cave_ids}")
    
    while True:
        try:
            choice = int(input("Choose a cave card ID to discard: "))
            if choice in hand_cave_ids:
                # Discard card
                player_hand["hand_caves"].remove(choice)
                return
            else:
                print(f"Invalid choice. Must be one of: {hand_cave_ids}")
        except ValueError:
            print("Please enter a valid integer.")

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

    human_discard_cave(player_hand["hand_caves"])
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

# TODO
def gain_benefit(player_hand, player_mat):
    '''Choice of Dragon Card, Cave Card, or Any Resource'''
    from init import ACTION_REGISTRY

    print("Choose a benefit to gain:")
    for i, benefit in enumerate(cave_card["benefits"], start=1):
        print(f"{i}. {benefit}")
    choice = input("Enter the number of the benefit you want to gain: ")
    do_benefit  = ACTION_REGISTRY[cave_card["benefits"][int(choice)-1]]
    do_benefit(player_hand, player_mat)
    return


def gain_cave_card(player_hand, player_mat):
    return

def gain_coin(player_hand, player_mat):
    player_hand["coins"] += 1
    return

def gain_crystal(player_hand, player_mat):
    player_hand["resources"]["crystals"] += 1
    return

def gain_dragon_card(player_hand, player_mat):
    return

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

def offer_to_pay_and_play_cave_card(player_hand, player_mat):
    return

def offer_3x(player_hand, player_mat):
    return

def swap_dragon_locations(player_hand, player_mat):
    return

def tuck_dragon_card_from_deck(player_hand, player_mat):
    return

def tuck_any_dragon_from_hand(player_hand, player_mat):
    # search for when resourcecached ability in dragon cards
    return