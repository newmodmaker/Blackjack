import random

# Card values and deck setup
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {
    **{str(n): n for n in range(2, 11)},
    **dict.fromkeys(['J', 'Q', 'K'], 10),
    'A': 11
}

def create_deck():
    return [(rank, suit) for suit in suits for rank in ranks]

def shuffle_deck(deck):
    random.shuffle(deck)

def deal_card(deck):
    return deck.pop()

def calculate_score(hand):
    score = sum(values[rank] for rank, _ in hand)
    aces = sum(1 for rank, _ in hand if rank == 'A')
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

# Player turn: show drawn card and handle bust
def player_turn(deck, hand):
    while True:
        score = calculate_score(hand)
        print(f"Your hand: {hand}  | Score: {score}")
        choice = input("Hit or Stand? (h/s): ").lower()

        if choice == 'h':
            card = deal_card(deck)
            hand.append(card)
            print(f"You drew: {card}")
            score = calculate_score(hand)
            if score > 21:
                print(f"Busted! Last card {card} took you to {score} points.")
                break

        elif choice == 's':
            break

        else:
            print("Invalid choice, type 'h' or 's'.")
    return hand

# Dealer turn: draw until score ≥ 17
def dealer_turn(deck, hand):
    while calculate_score(hand) < 17:
        card = deal_card(deck)
        hand.append(card)
        print(f"Dealer drew: {card}")
    print(f"Dealer's hand: {hand}  | Score: {calculate_score(hand)}")
    return hand

# Ask for bet and validate
def place_bet(bankroll):
    while True:
        print(f"Your current balance: ${bankroll}")
        try:
            bet = int(input("How much would you like to bet? $"))
            if 1 <= bet <= bankroll:
                return bet
            print("Bet must be between $1 and your current balance.")
        except ValueError:
            print("Enter a valid number (e.g. 10).")

# Determine winner and update bankroll
def determine_winner(player_hand, dealer_hand, bet, bankroll):
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    if player_score > 21:
        print("You busted, you lose your bet.")
        return bankroll - bet
    if dealer_score > 21 or player_score > dealer_score:
        print(f"You win! You gain ${bet}.")
        return bankroll + bet
    if player_score < dealer_score:
        print("Dealer wins, you lose your bet.")
        return bankroll - bet

    print("Push, your bet is returned.")
    return bankroll

# Main game loop per round
def play_game(bankroll):
    bet = place_bet(bankroll)
    deck = create_deck()
    shuffle_deck(deck)

    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    player_hand = player_turn(deck, player_hand)
    if calculate_score(player_hand) <= 21:
        dealer_turn(deck, dealer_hand)

    new_bankroll = determine_winner(player_hand, dealer_hand, bet, bankroll)
    print(f"New balance: ${new_bankroll}\n")
    return new_bankroll

if __name__ == "__main__":
    bankroll = 100
    while bankroll > 0:
        bankroll = play_game(bankroll)
        again = input("Play again? (y/n): ").lower()
        if again != 'y':
            print("Thanks for playing! Goodbye.")
            break
    if bankroll <= 0:
        print("You're out of money. Game over.")
