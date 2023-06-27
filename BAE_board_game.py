#IMPORTING STATEMENTS
from random import random
from random import randint

#DEFINE BOARD SIZE
board_size = 20

#PLAYERS
#Creating the players
num_players = 4

#Player funds for each player
player_funds = [250] * num_players

#players starting positions for each player
players_position = [0] * num_players


#PROPERTY
#Prices, rent(20%), category (3 properties of each length of square board), owner
property_prices = {
    "Property 1": {"cost": 100, "rent": 20, "category": "Category 1", 'owner': None},
    "Property 2": {"cost": 150, "rent": 30, "category": "Category 1", 'owner': None},
    "Property 3": {"cost": 200, "rent": 40, "category": "Category 1", 'owner': None},
    "Property 4": {"cost": 250, "rent": 50, "category": "Category 2", 'owner': None},
    "Property 5": {"cost": 200, "rent": 40, "category": "Category 2", 'owner': None},
    "Property 6": {"cost": 120, "rent": 24, "category": "Category 2", 'owner': None},
    "Property 7": {"cost": 200, "rent": 40, "category": "Category 3", 'owner': None},
    "Property 8": {"cost": 180, "rent": 36, "category": "Category 3", 'owner': None},
    "Property 9": {"cost": 100, "rent": 20, "category": "Category 3", 'owner': None},
    "Property 10": {"cost": 150, "rent": 30, "category": "Category 4", 'owner': None},
    "Property 11": {"cost": 200, "rent": 40, "category": "Category 4", 'owner': None},
    "Property 12": {"cost": 200, "rent": 40, "category": "Category 4", 'owner': None},
}
#number of properties
num_properties = 12

#property ownership as per board size
property_ownership = [-1] * num_properties

#category_ownership = category[player]
# Function to check if a player owns all properties in a category
def owns_all_properties(player, category):
    return all(prop_info["owner"] == player for prop_info in property_prices.values() if prop_info["category"] == category)

#CREATING THE DICE
#creating a function to roll the dice
def roll_dice():
    return randint(1,6)


#EFFECTS
effect_tiles = ['Go forward 2 spaces',
                 'Go forward 3 spaces',
                 'Gain 50',
                 'Pay 10 in fees',
                 'Go to start and gain 50',
                 'Roll again']

#Effects functions
def effect_function(player, players_position):
    #establish effect index with players position relative to board size
    effect_index = players_position[player] % board_size
    #establish the effect for the index
    effect = effect_tiles[effect_index]

#Create statements for each effect
    if effect == 'Go forward 2 spaces':
        players_position[player] += 2
    elif effect == 'Go forward 3 spaces':
        players_position[player] += 3
    elif effect == 'Gain 50':
        player_funds[player] += 50
    elif effect == 'Pay 10 in fees':
        player_funds[player] -= 10
    elif effect == 'Go to start and gain 50':
        players_position[player] = 0
        player_funds[player] += 50
    elif effect == 'Roll again':
        return True
    
    print(f'Player {player+1} landed on an effects tile: {effect}')


#THE GAME ----

#define current players position
current_player = 0

running = True

#The loop
while running:
#Iterating over each player
    #define players and rolls
    player = current_player % num_players
    #roll the dice, ensuring rolls are < 3
    
    dice_roll = roll_dice()

    #update the players position appropriate to board size
    players_position[player] += dice_roll
    players_position[player] %= board_size
        
    #if player >19 places on the board size, reset to 0 and give 50
    if players_position[player] == 0:
        player_funds[player] += 50

    #if a player lands on an effects tile
    if players_position[player] < len(effect_tiles):
        #effect_function(player, players_position)
        roll_again = effect_function(player, players_position)

        if roll_again:
            rolls = 1
            while rolls <3:
                dice_roll = roll_dice()
                players_position[player] += dice_roll
                players_position[player] %= board_size
                
                if players_position[player] < len(effect_tiles):
                    roll_again = effect_function(player, rolls, players_position)

                    if not roll_again:
                        break

                rolls +=1


    #Checking if a player lands on a property
    property_index = (players_position[player]-1) % num_properties
    property_name = f'Property {property_index + 1}'

    #IF A PROPERTY IS OWNED
    if property_name in property_prices and property_ownership[property_index] != -1:
        #decipher ownership
        if property_ownership[property_index] != player:
            owner = property_ownership[property_index]
            #define rent amount
            property_rent = property_prices[property_name]["rent"]

            #check if a player owns all properties in a category
            category = property_prices[property_name]['category']
            owns_all = owns_all_properties(player, category)

            #if owns all in one category, doulbe the rent
            if owns_all:
                property_rent*2
                print(f'Rent has doubled.')
            else:
                property_rent

            #pay rent
            player_funds[player] -= property_rent
            player_funds[owner] += property_rent
            
            #Update the display with rent paid, and new fund amount
            print(f'Player {player+1}: You have paid Player{owner+1} {property_rent} in rent. You now have {player_funds[player]}.')
            print(f'Player{owner+1}, you now have {player_funds[owner]}.')



#IF A PROPERTY IS UNOWNED
    if property_name in property_prices and property_ownership[property_index] == -1:
    #Ask the player if they would like to purchase the property
        #define property cost at appropriate index
        property_cost = property_prices[property_name]["cost"]
        #property_cost = property_prices[property_name]["cost"]
        purchase_choice = input(f'Player {player+1}, you have landed on an unowned property at {property_index+1}\n'
                        f'This property costs {property_cost}. You have {player_funds[player]}. Do you want to buy it? (y/n)')
        
        if purchase_choice.lower() == 'y':
        #Check the player has enough money to buy
            #if player has enough money:
            if player_funds[player] >= property_cost:
                #deduct from players funds
                player_funds[player] -= property_cost
                #update ownership
                property_ownership[property_index] = player
                #update owner value
                property_prices[property_name]['owner'] = player
                #confirm the property has been bought
                print(f'You have purchased {property_name}')
            #if not enough money
            else:
                print('You do not have enough money to purchase this property.')
        
    
    #display the player, dice roll and current position
    print(f"Player {player+1}: Your current position is {players_position[player]}. You have {player_funds[player]}")
    #Make display easier to navigate & ready
    print('-')
    #update current player
    current_player += 1
    
    #Kicking players out of the game
    #If a player has no more money
    if player_funds[player] < 0:
        print(f'Player {player+1} is out of money and has been removed from the game.')

        #set properties as unowned
        for prop in property_prices:
            #accessing the property index and splitting it
            property_index = int(prop.split()[1]) -1
            property_ownership[property_index] = -1

        # Store the index of the player being removed
        removed_player_index = player

        #remove player from game
        del player_funds[player]
        del players_position[player]
        num_players -= 1
        current_player = current_player % num_players

        # Adjust player indices
        for i in range(num_players - 1):
            if i >= removed_player_index:
                players_position[i] = players_position[i + 1]

        #check if there is one player left (the winner)
        if num_players == 1:
            winner = -1
            for i, funds in enumerate(player_funds):
                if funds >= 0:
                    winner = i
                    break
            if winner != -1:
                print(f'Player {winner+1} has won! with {player_funds[winner]} in their bank!')
                running = False
    
    #IF ALL PROPERTIES ARE OWNED
    if all(ownership != -1 for ownership in property_ownership):
        print('All properties are owned.')
        running = False

        #End the game and determine winner
        max_money = max(player_funds)
        winners = [i + 1 for i, fund in enumerate(player_funds) if fund == max_money]
        if len(winners) == 1:
            print(f'Player {winners[0]} wins the game with {player_funds[winners[0] - 1]}')
            running = False
        else:
            print(f'Its a tie.')
            print(f'Player {player} : {player_funds} funds')
            running = False

#The end.


    