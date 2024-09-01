'''
My program will be a game of blackjack against a computer dealer, the program will start with 
a menu that allows the user to start a game, display the current leaderboard, and exit the 
program. The main game will consist of the user deciding to hit or stand and will update the 
command line GUI every time a move is made. There won't be an option to double down in this 
version since no betting is involved. While it's the dealer's turn, the program will display 
what the dealer chose to do and prompt the user to press enter before continuing to the next 
action to allow them time to read what happened. The game will keep track of how many times 
the user beats the dealer before they lose and write that to the leaderboard file if it is 
one of the top 10. The program will also write the amount of times they won to another file 
which gets overwritten every time a new game is played. The leaderboard option in the menu 
will display the leaderboard and prompt the user to return to the menu.
'''

import os
from random import shuffle

spacer = '-'*12
running = True
playing = False
wins = 0


def main_menu():
    """displays the main menu of the game
    """    
    global wins, playing, running
    # clear the screen
    clear()
    # display menu ui
    print(f'{spacer} Black Jack {spacer}')
    print('1: Start game')
    print('2: Display leaderboard')
    print('3: Exit')
    valid = False
    while not valid:
        # prompt the user for their choice
        choice = input('Enter your choice: ')
        # check which choice they made
        match choice:
            case '1':
                valid = True
                # start the game
                playing = True
                wins = 0
                while playing:
                    start_game()
            case '2':
                valid = True
                # display the leaderboard
                show_leaderboard()
            case '3':
                valid = True
                # exit the program
                running = False
            case _:
                print('invalid choice, try again')
    
def start_game():
    """the main game
    """    
    global wins
    # create and shuffle deck
    suits = ["H", "D", "C", "S"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = [(rank, suit) for suit in suits for rank in ranks]
    shuffle(deck)
    #clear the screen
    clear()
    # deal both hands
    player_hand = []
    dealer_hand = []
    for i in range(2):
        player_hand.append(deck.pop(0))
        dealer_hand.append(deck.pop(0))
    
    print(f'{spacer} Player Turn {spacer}')
    # start the player turn loop
    player_turn = True
    v = hand_value(player_hand)
    while player_turn and hand_value(player_hand) < 21:
        # print dealer hand
        print('--- Dealer Hand ---')
        print(f'{"".join(dealer_hand[0])}, X')
        # print player hand
        print('--- Your Hand ---')
        print(hand_str(player_hand))
        # prompt the player to hit or stand
        print('1: hit \n2: stand')
        valid = False
        while not valid:
            choice = input('Enter your choice: ')
            match choice:
                # if hit then draw a card
                case '1':
                    valid = True
                    player_hand.append(deck.pop(0))
                # if stand, stop the player turn loop
                case '2':
                    valid = True
                    player_turn = False
                # if invalid, return to choice prompt
                case _:
                    print('invalid choice, try again')

    # if card value is over 21, stop the game
    if hand_value(player_hand) > 21:
        print('bust, you lose')
        quit_game(wins)
        print(f'You beat the dealer {wins} times')
        input('press enter to return to menu')
        return
    # if card value is 21, stop the player's turn
    elif hand_value(player_hand) == 21:
        print('--- Your Hand ---')
        print(hand_str(player_hand))
        print('BlackJack')
        player_turn = False
        input('press enter to continue')
    
    
    print(f'{spacer} Dealer Turn {spacer}')
    
    # start the dealer turn loop
    while not player_turn and hand_value(dealer_hand) < 21:
        dv = hand_value(dealer_hand)
        # display the dealer's hand
        print('--- Dealer Hand ---')
        print(hand_str(dealer_hand))
        # decide whether to hit or stand
        if hand_value(dealer_hand) > hand_value(player_hand):
            player_turn = True
            print('stand')
        else:
            dealer_hand.append(deck.pop(0))
            print('hit')
        
        # prompt user to continue
        input('press enter to continue')

    # if over 21 or less than player's score, player wins
    if hand_value(dealer_hand) > 21 or hand_value(dealer_hand) < hand_value(player_hand):
        # display final dealer hand
        print('--- Dealer Hand ---')
        print(hand_str(dealer_hand))
        if hand_value(dealer_hand) > 21:
            print('Bust')
        print('You Win!')
        # add to player's win total
        wins += 1
        # prompt the player to start another game
        print(f'You beat the dealer {wins} times')
        choice = input('play again? (Y/N)')
        match choice.lower():
            case 'y':
                pass
            case 'n':
                quit_game(wins)
                return
    
    # if equal, prompt the player to start another game
    elif hand_value(dealer_hand) == hand_value(player_hand):
        # display final dealer hand
        print('--- Dealer Hand ---')
        print(hand_str(dealer_hand))
        
        print('You tied')
        print(f'You beat the dealer {wins} times')
        choice = input('play again? (Y/N)')
        match choice.lower():
            case 'y':
                pass
            case 'n':
                quit_game(wins)
                return
    
    # if greater than player's score, player loses
    else:
        print('You lose')
        # end the game and go back to menu
        quit_game(wins)
        print(f'You beat the dealer {wins} times')
        input('press enter to return to menu')
        

def hand_value(hand):
    """calculates the value of a given hand

    Args:
        hand (list[tuple(str)]): the hand to use for the calculation

    Returns:
        int: the value of the hand
    """    
    # set initial values for high and low value
    high_value = 0
    low_value = 0
    # variable to check if there is already an ace in the hand
    a = False
    # loop through each card in the hand
    for card in hand:
        # check if the card is a royal or 10, length of card string can only be 3 for a 10
        if card[0] in ['J', 'Q', 'K'] or len(card) == 3:
            high_value += 10
            low_value += 10
        # check if card is an ace
        elif card[0] == 'A':
            if not a:
                high_value += 11
                low_value += 1
            else:
                high_value += 1
                low_value += 1
            # set that an ace was found
            a = True
        # add value of any other number card to values
        else:
            high_value += int(card[0])
            low_value += int(card[0])
    # check which value to return
    if high_value <= 21:
        return high_value
    else:
        return low_value

def hand_str(hand):
    """gets the string representaion of a hand

    Args:
        hand (list[tuple(str)]): the hand to be represented

    Returns:
        str: the string representaion of the hand
    """        
    return ', '.join([''.join(card) for card in hand])

def show_leaderboard():
    """displays the leaderboard if it exists
    """    
    clear()
    try:
        with open('lb.txt', 'r') as lb:
            print(f'{spacer} Leaderboard {spacer}')
            print('{0:^10} | {1:^10}'.format('Name','Score'))
            print(spacer*2)
            for line in lb.readlines():
                line = line.strip('\n').split(',')
                name = line[0]
                score = line[1]
                print('{0:^10} |  {1:^10}'.format(name, score))
        lb.close()
    except FileNotFoundError:
        print("leaderboard doesn't exist yet, play a game first")
    input('press enter to return to menu')
            

def quit_game(wins):
    """checks if the player should be on the leaderboard and puts them there if so

    Args:
        wins (int): the ammount of wins the player has
    """    
    global playing
    playing = False
    changed = False
    print(f'Thank you for playing\nYou had {wins} wins')
    # check if leaderboard file exists and if not, create one
    try:
        open('lb.txt', 'x')
    except FileExistsError:
        pass
    # read leaderboard file
    leaderboard = open('lb.txt', 'r')
    lb = leaderboard.readlines()
    leaderboard.close()
    # check if player's score should be put on the leaderboard
    i = 0
    if len(lb) < 10:
        name = input('Youre on the leaderboard!!\nPlease enter your name: ')
        valid = True
        # check if name is valid for the leaderboard
        if len(f'{name},{wins}\n') > 20:
            valid = False
        inserted = False
        if valid:
            for line in lb:
                if int(line.strip('\n').split(',')[1]) < wins:
                    lb.insert(i, f'{name},{wins}\n')
                    inserted = True
                    break
                i += 1
            if not inserted:
                lb.append(f'{name},{wins}\n')
            changed = True
    else:
        for line in lb:
            if int(line.split(',')[1]) < wins:
                # if so, write it to the right spot and push all lower scores back one
                name = input('Youre on the leaderboard!!\nPlease enter your name: ')
                valid = True
                # check if name is valid for the leaderboard
                if len(f'{name},{wins}\n') > 20:
                    valid = False
                if valid:
                    lb.insert(i, f'{name},{wins}\n')
                    lb.pop(10)
                    changed = True
    # write leaderboard back to file if it was changed
    if changed:
        leaderboard = open('lb.txt', 'w')
        for line in lb:
            leaderboard.write(line)
        leaderboard.close()
        
    with open('cps109_a1_output.txt', 'w') as f:
        f.write(f'You beat the dealer {wins} times')

def clear():
    os.system('cls')
        
def main():
    while running:
        main_menu()

if __name__ == '__main__':       
    main()