import random

# define card class attributes and methods
class Card:
    def __init__(self, value, numeral, suit):
        self.value = value
        self.numeral = numeral
        self.suit = suit
    # method to display attributes of a card
    def show(self):
        print(f"{self.numeral} of {self.suit}")
        return self

# define player class attributes and methods
class Player:
    def __init__(self, name, position):
        self.name = name
        # a list of cards
        self.hand = []
        self.points = 0
        self.position = position
    # method to sort the cards in a player's hand
    def sort_cards(self):
        self.hand.sort(key=lambda card: card.value)
        return self
    # method to find four-of-a-kinds, remove them from the player's hand, and award the player a point
    def remove_sets(self):
        # flag to determine if a set was found
        flag = True
        while flag and len(self.hand) > 3:
            flag = False
            for i in range(3, len(self.hand)):
                # if four cards in a row are the same
                if self.hand[i].value == self.hand[i-1].value and self.hand[i].value == self.hand[i-2].value and self.hand[i].value == self.hand[i-3].value:
                    # remove all four cards from the hand
                    for j in range(4):
                        for k in range(i-3, len(self.hand)-1):
                            self.hand[k] = self.hand[k+1]
                        self.hand.pop()
                    # award the player a point
                    self.points += 1
                    print(f"{self.name} completed a set!")
                    flag = True
                    break
        return self
    # method to display attributes of human player
    def show_all(self):
        position = str(self.position)
        print("\n", "-"*30, self.name, "(player #"+position+")", "-"*10, "Points:", self.points, "-"*30)
        for card in self.hand:
            card.show()
        return self
    # method to display attributes of computer players
    def show_some(self):
        position = str(self.position)
        print("\n", "_"*30, self.name, "(player #"+position+")", "-"*10, "Points:", self.points, "_"*30)
        print("Number of cards in hand:", len(self.hand))
        return self

# define deck class attributes and methods
class Deck:
    def __init__(self, name):
        self.name = name
        # a list of cards
        self.deck = []
        suit_list = ["hearts", "spades", "diamonds", "clubs"]
        numeral_list = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        for suit in suit_list:
            for value in range(1, 14):
                i = value - 1
                numeral = numeral_list[i]
                self.deck.append(Card(value, numeral, suit))
    # method for shuffling the deck
    def shuffle(self):
        random.shuffle(self.deck)
        return self
    # method for dealing one card to one player
    def deal(self, Player):
        card = self.deck.pop()
        Player.hand.append(card)
        return self
    # method for dealing one card to player 1, and displaying the attributes of that card
    def deal_show(self, Player):
        card = self.deck.pop()
        Player.hand.append(card)
        print("You drew:", end=" ")
        card.show()
        return self
    # method for displaying the attributes of all the cards in the deck
    def show(self):
        print("\n", "*"*30, self.name, "*"*30)
        for card in self.deck:
            card.show()
        return self

# define game class attributes and methods
class Game:
    def __init__(self):
        # a list of players
        self.players = []
        name = input("\n Player 1, enter your name: ")
        player1 = Player(name, 1)
        player2 = Player("The Jack", 2)
        player3 = Player("The Queen", 3)
        player4 = Player("The King", 4)
        self.players.append(player1)
        self.players.append(player2)
        self.players.append(player3)
        self.players.append(player4)
    # method to display various attributes of the players
    def show(self):
        self.players[0].sort_cards().remove_sets().show_all()
        for i in range(1, len(self.players)):
            self.players[i].sort_cards().remove_sets().show_some()
        return self

# function to determine if there are enough active players in the game to continue playing
def active_players(game):
    count = 0
    for player in game.players:
        if len(player.hand) > 0:
            count += 1
    return count

# function to define game play
def play_game():
    print("\n", "Welcome to GO FISH!")
    print("Collect the most four-of-a-kinds to win. Ask other players for cards to complete sets. Game ends when there are no more cards in the deck.")
    deck = Deck("Game Deck")
    deck.shuffle()
    game = Game()
    print("\n")
    # deal 7 cards to each player
    for i in range(7):
        for j in range(len(game.players)):
            deck.deal(game.players[j])
        print("Dealing...")
    game.show()
    print("\n", "There are", len(deck.deck), "more cards in the deck.")

    # determine how long game will last
    # flag to exit game when there are no longer enough players
    active_players_flag = True
    while len(deck.deck) > 0 and active_players_flag:
        # human player's turn
        # flag to exit turn once Go Fish! is called
        go_fish_flag = False
        # determine how long turn will last
        while not go_fish_flag and active_players_flag:
            # player will only take their turn if they have cards in their hand
            if len(game.players[0].hand) > 0:
                # choose an opponent
                opponent_choices = [2, 3, 4]
                # flag to determine if a valid opponent has been chosen
                opponent_flag = False
                while not opponent_flag:
                    result = input(f"\n {game.players[0].name}, from whom would you like to ask a card? (enter the player's number)   ")
                    # verify that input is a digit
                    valid_result = result.isdigit()
                    if valid_result:
                        opponent = int(result)
                        # verify that input is a player in the game
                        for i in range(len(opponent_choices)):
                            if opponent == opponent_choices[i]:
                                for j in range(len(game.players)):
                                    if opponent == game.players[j].position:
                                        opponent_player = game.players[j]
                                        # verify whether the chosen opponent is an active player (has cards in their hand)
                                        if len(opponent_player.hand) == 0:
                                            print(f"{opponent_player.name} does not have any cards.", end=" ")
                                        else:
                                            # valid opponent found
                                            opponent_flag = True
                    # provide messages for player experience
                        if opponent_flag:
                            print(f"You have chosen to ask {opponent_player.name} for a card.")
                        else:
                            print("Invalid selection. Please choose again.")
                    else:
                        print("Invalid selection. Please choose again. From whom would you like to ask a card? (enter the player's number) ")
                # choose a card
                request_choices = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
                # flag to determine if a valid card has been chosen
                request_flag = False
                while not request_flag:
                    request = input(f"\n {game.players[0].name}, which card would you like? (Press 'A' for Ace, '2' for 2, '3' for 3 ... 'J' for Jack, 'Q' for Queen, 'K' for King)   ")
                    # make all input uppercase for consistency
                    request = request.upper()
                    # verify that input is a card in the game
                    for i in range(len(request_choices)):
                        if request == request_choices[i]:
                            # verify that input is a card in player's hand
                            for j in range(len(game.players[0].hand)):
                                if request == game.players[0].hand[j].numeral:
                                    # valid card found
                                    request_flag = True
                    # provide messages for player experience
                            if not request_flag:
                                print("You must choose a card value that you currently hold in your hand.", end=" ")
                    if request_flag:
                        print(f"You have asked for {request}'s.")
                    else:
                        print("Invalid selection. Please choose again.")
                # flag to determine if the opponent has the chosen card in their hand
                flag = True
                # list of cards found in opponent's hand that match the chosen card
                requested_cards = []
                while flag and len(opponent_player.hand) > 0:
                    flag = False
                    # check the opponent's hand for the requested card
                    for i in range(len(opponent_player.hand)):
                        # if found, remove the card from the opponent's hand and put it in the list
                        if request == opponent_player.hand[i].numeral:
                            requested_cards.append(opponent_player.hand[i])
                            for j in range(i, len(opponent_player.hand)-1):
                                opponent_player.hand[j] = opponent_player.hand[j+1]
                            opponent_player.hand.pop()
                            flag = True
                            break
                # put found cards in player's hand
                if len(requested_cards) == 1:
                    print("\n", f"{opponent_player.name} has {len(requested_cards)} {request}.")
                    requested_cards[0].show()
                    game.players[0].hand.append(requested_cards[0])
                elif len(requested_cards) > 1:
                    print("\n", f"{opponent_player.name} has {len(requested_cards)} {request}'s.")
                    for i in range(len(requested_cards)):
                        requested_cards[i].show()
                        game.players[0].hand.append(requested_cards[i])
                # if no cards were found, provide message, deal player a new card, and set flag to end player's turn
                else:
                    print("\n", f"{opponent_player.name} does not have any {request}'s. GO FISH!")
                    deck.deal_show(game.players[0])
                    print("\n", "There are", len(deck.deck), "more cards in the deck.")
                    go_fish_flag = True
                game.show()
                # determine if there are still enough active players for the game to continue
                count = active_players(game)
                if count < 2:
                    active_players_flag = False
            # message provided, and flag is set to skip turn, if player's hand is empty
            else:
                print("\n", "You have no cards in your hand. Your turn is skipped.")
                go_fish_flag = True
            print("\n")

        # computers's turns
        for position in range(2, len(game.players)+1):
            print("$"*90)
            ready = input("Press enter to continue with the game.")
            # determine whose turn it is
            for i in range(len(game.players)):
                if position == game.players[i].position:
                    current_player = game.players[i]
            print("current player:", current_player.name)
            # flag to exit turn once Go Fish! is called
            go_fish_flag = False
            # determine how long turn will last
            while not go_fish_flag and active_players_flag:
                # player will only take their turn if they have cards in their hand
                if len(current_player.hand) > 0:
                    # choose an opponent
                    opponent_choices = []
                    for opponent_position in range(1, len(game.players)+1):
                        if opponent_position != current_player.position:
                            opponent_choices.append(opponent_position)
                    # flag to determine if a valid opponent has been chosen
                    opponent_flag = False
                    while not opponent_flag:
                        rand_num = random.randint(0,len(opponent_choices)-1)
                        opponent = opponent_choices[rand_num]
                        for i in range(len(game.players)):
                            if opponent == game.players[i].position:
                                opponent_player = game.players[i]
                        # verify whether the chosen opponent is an active player (has cards in their hand)
                        if len(opponent_player.hand) > 0:
                            # valid opponent found
                            opponent_flag = True
                            print("opponent:", opponent_player.name)
                    # choose a card
                    request_choices = ["A", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
                    # flag to determine if a valid card has been chosen
                    request_flag = False
                    while not request_flag:
                        rand_num = random.randint(0, len(request_choices)-1)
                        request = request_choices[rand_num]
                        # verify that chosen card is a card in player's hand
                        for i in range(len(current_player.hand)):
                            if request == current_player.hand[i].numeral:
                                # valid card found
                                request_flag = True
                        if request_flag:
                            print("requested card:", request)
                    # flag to determine if the opponent has the chosen card in their hand
                    flag = True
                    # list of cards found in opponent's hand that match the chosen card
                    requested_cards = []
                    while flag and len(opponent_player.hand) > 0:
                        flag = False
                        # check the opponent's hand for the requested card
                        for i in range(len(opponent_player.hand)):
                            # if found, remove the card from the opponent's hand and put it in the list
                            if request == opponent_player.hand[i].numeral:
                                requested_cards.append(opponent_player.hand[i])
                                for j in range(i, len(opponent_player.hand)-1):
                                    opponent_player.hand[j] = opponent_player.hand[j+1]
                                opponent_player.hand.pop()
                                flag = True
                                break
                    # put found cards in player's hand
                    if len(requested_cards) == 1:
                        print(f"{opponent_player.name} has {len(requested_cards)} {request}.")
                        requested_cards[0].show()
                        current_player.hand.append(requested_cards[0])
                    elif len(requested_cards) > 1:
                        print(f"{opponent_player.name} has {len(requested_cards)} {request}'s.")
                        for i in range(len(requested_cards)):
                            requested_cards[i].show()
                            current_player.hand.append(requested_cards[i])
                    # if no cards were found, provide message, deal player a new card, and set flag to end player's turn
                    else:
                        print(f"{opponent_player.name} does not have any {request}'s. GO FISH!")
                        deck.deal(current_player)
                        go_fish_flag = True
                        print("\n", "There are", len(deck.deck), "more cards in the deck.")
                    game.show()
                    # determine if there are still enough active players for the game to continue
                    count = active_players(game)
                    if count < 2:
                        active_players_flag = False
                    if not go_fish_flag and active_players_flag:
                        print("*"*30)
                # message provided, and flag is set to skip turn, if player's hand is empty
                else:
                    print(f"{current_player.name} does not have any cards. Skip turn!")
                    go_fish_flag = True
                print("\n")
    # declare winner
    game.players.sort(key=lambda player: player.points, reverse=True)
    # list of winners, in case there is a tie
    winners = [game.players[0]]
    max_points = game.players[0].points
    for i in range(1, len(game.players)):
        if game.players[i].points >= max_points:
            max_points = game.players[i].points
            winners.append(game.players[i])
    # display messages for end-of-game player experience
    if len(winners) == 1:
        print(f"The winner is {winners[0].name}!")
    else:
        print("The winners are:")
        for i in range(len(winners)):
            print(f"{winners[i].name}!")
    for i in range(len(game.players)):
        print("Name:", game.players[i].name, "*"*10, "Points:", game.players[i].points)
play_game()
