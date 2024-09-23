import random
import os

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] 
deck = cards * 4

playersHand = []
dealersHand = []
# This will assign the integer value the corresponding card value
def assignValue(card):
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)
# Provides some logic for handling the aces when the hand value goe over 21 
def adjustForAces(value, ace_count):
    while value > 21 and ace_count > 0:
        value -= 10
        ace_count -= 1
    return value
# When the game runs out of cards this will be called to reshuffle the deck
def reshuffle_deck():
    global deck
    deck = cards * 4
    random.shuffle(deck)
    print("The deck has been reshuffled.")
# This will deal a card 
def deal():
    if len(deck) == 0:
        reshuffle_deck()
    dealtCard = random.choice(deck) # Random choice within the 52 card deck
    deck.remove(dealtCard)
    return dealtCard
# Using the deal function, this will add it to whatever list is passed through as a parameter, both int and chars
def deal_and_add_card(hand, value_list, ace_count):
    new_card = deal()
    hand.append(new_card)
    card_value = assignValue(new_card)
    value_list.append(card_value)
    if card_value == 11:
        ace_count += 1
    return card_value, ace_count
# This function will deal 2 cards to the player intially, then they will have the chance to hit or stand, or if they are lucky to split into 2 hands
def playerHand():
    value = []
    ace_count = 0
    # Deals intial hand
    deal_and_add_card(playersHand, value, ace_count)
    deal_and_add_card(playersHand, value, ace_count)

    total = sum(value)
    print(f"Player's hand {playersHand}. Total: {total}") # Show the hand and the value

    if playersHand[0] == playersHand[1]:  # Provides the player with the option to split
        split = input("Do you want to split your hand? (y/n): ").lower()
        if split == "y":
            value2, firstHandTotal, secondHandTotal = handle_split(playersHand[0], playersHand[1], value, ace_count)
            return firstHandTotal, secondHandTotal  # Return both hand totals

    return hit_or_stand(playersHand, value, ace_count)
# This provides the way the 2 seperate hands would be handled moving forward witht the game
def handle_split(firstCard, secondCard, value, ace_count):
    value.pop() 
    playersHand.pop()  # Removes the second card from the original hand

    value2 = []
    playerHandTwo = []
    playerHandTwo.append(secondCard)
    card_value = assignValue(secondCard)
    value2.append(card_value)
    # This runs similar to the orginal player hand function except that it has two hands
    deal_and_add_card(playersHand, value, ace_count)
    deal_and_add_card(playerHandTwo, value2, ace_count)

    print(f"Players first hand {playersHand}. Total: {sum(value)}") # Show the hand 1 and the value
    firstHandTotal = hit_or_stand(playersHand, value, ace_count)

    print(f"Players second hand {playerHandTwo}. Total: {sum(value2)}") # Show the hand 2 and the value
    secondHandTotal = hit_or_stand(playerHandTwo, value2, ace_count)

    return value2, firstHandTotal, secondHandTotal  # Return hand values and totals

# Hit or stand logic for the player
def hit_or_stand(hand, value, ace_count):
    while True:
        total = sum(value)
        total = adjustForAces(total, ace_count)

        if total > 21:
            print(f"Your current hand: {hand}. (Total: {total})")
            print("You busted!")
            return total  # Exits the function upon busting so player cannot keep hitting after a loss

        hit = input("Hit? (y/n): ").lower() 
        # Deals more cards or no cards based on the players answer
        if hit == "y":
            deal_and_add_card(hand, value, ace_count) 

            total = sum(value)
            total = adjustForAces(total, ace_count)

            print(f"Your current hand: {hand}. (New total: {total})")

            if total > 21:
                print("You busted!")
                return total  # Exit function when busting

        elif hit == "n":
            print(f"You chose to stand. Your final total is {total}.")
            return total  # Exit function and return final total

        else:
            print("Invalid input. Please enter 'y' to hit or 'n' to stand.")

# This function will only reveal the dealer's first card so the player can deterine thier next move
def dealerFirstCard():
    firstCard = deal()
    dealersHand.append(firstCard)
    print(f"Dealer's reveals '{firstCard}'. Total: {assignValue(firstCard)}")
    return assignValue(firstCard)

# Reveals the rest of the dealer's hand and will hit until it has a value passed 17
def restOfDealerHand(firstCardValue):
    value = [firstCardValue]
    ace_count = 0
    if firstCardValue == 11:  # If the first card was an Ace
        ace_count += 1

    secondCard = deal()
    dealersHand.append(secondCard)
    secondCardValue = assignValue(secondCard)
    value.append(secondCardValue)
    if secondCardValue == 11:  # If the second card was an Ace
        ace_count += 1

    total = sum(value)

    print(f"Dealer reveals {secondCard}. Dealer's hand: {dealersHand}. Total: {total}") # Show the dealer's intial hand

    while total < 17: # Keep hitting until the hand value is at least 17
        newCard = deal()
        dealersHand.append(newCard)
        card_value = assignValue(newCard)
        value.append(card_value)
        if card_value == 11:  # If the new card was an Ace
            ace_count += 1
        total = sum(value)
        total = adjustForAces(total, ace_count)  # Adjust for aces if necessary
        print(f"Dealer hits and gets {newCard}. (New total: {total})")

    return total  # Return adjusted total

# Determine the winner for both hands if split, or single hand otherwise
def winner(playerTotal, dealerTotal, hand_number=1):
    if dealerTotal > 21:
        print(f"Dealer Bust! Player Hand {hand_number} Wins!")
    elif playerTotal > dealerTotal:
        print(f"Player Hand {hand_number} wins!")
    elif playerTotal < dealerTotal:
        print(f"Dealer wins against Player Hand {hand_number}!")
    else:
        print(f"Push with Player Hand {hand_number}!")  # Tie

# Main game logic
def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Cross-platform clear
        playersHand.clear()
        dealersHand.clear()

        # Simulate dealer and player hands
        dealerHandTotal = dealerFirstCard()
        playerHandTotal = playerHand()  # This now returns totals of both hands if split

        # Check if the player has split hands
        if isinstance(playerHandTotal, tuple):
            # The player split, so handle both hands separately
            firstHandTotal, secondHandTotal = playerHandTotal

            # Check each hand against the dealer's hand
            print(f"\nChecking Player's first hand against the dealer.")
            if firstHandTotal > 21:
                print("Player's first hand Bust! Dealer Wins!")
            else:
                dealerHandTotal = restOfDealerHand(dealerHandTotal)
                winner(firstHandTotal, dealerHandTotal, hand_number=1)

            print(f"\nChecking Player's second hand against the dealer.")
            if secondHandTotal > 21:
                print("Player's second hand Bust! Dealer Wins!")
            else:
                winner(secondHandTotal, dealerHandTotal, hand_number=2)

        else:
            # No split, regular gameplay
            if playerHandTotal > 21:
                print("Player Bust! Dealer Wins!")
            else:
                dealerHandTotal = restOfDealerHand(dealerHandTotal)
                winner(playerHandTotal, dealerHandTotal)

        # Ask for a new game
        playAgain = input("New Deal? (y/n): ").lower()
        if playAgain == 'n':
            return

if __name__ == "__main__":
    main()
