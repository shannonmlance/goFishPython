import random

class Card:
    def __init__(self, value, numeral, suit):
        self.value = value
        self.numeral = numeral
        self.suit = suit
    def show(self):
        print(f"{self.numeral} of {self.suit}")
        return self

class Player:
    def __init__(self, name, position):
        self.name = name
        self.hand = []
        self.points = 0
        self.position = position
    def sort_cards(self):
        self.hand.sort(key=lambda card: card.value)
        return self
    def remove_sets(self):
        flag = True
        while flag and len(self.hand) > 3:
            flag = False
            for i in range(3, len(self.hand)):
                if self.hand[i].value == self.hand[i-1].value and self.hand[i].value == self.hand[i-2].value and self.hand[i].value == self.hand[i-3].value:
                    for j in range(4):
                        for k in range(i-3, len(self.hand)-1):
                            self.hand[k] = self.hand[k+1]
                        self.hand.pop()
                    self.points += 1
                    print(f"{self.name} completed a set!")
                    flag = True
                    break
        return self
    def show_all(self):
        position = str(self.position)
        print("\n", "-"*30, self.name, "(player #"+position+")", "-"*10, "Points:", self.points, "-"*30)
        for card in self.hand:
            card.show()
        return self
    def show_some(self):
        position = str(self.position)
        print("\n", "_"*30, self.name, "(player #"+position+")", "-"*10, "Points:", self.points, "_"*30)
        print("Number of cards in hand:", len(self.hand))
        return self

class Deck:
    def __init__(self, name):
        self.name = name
        self.deck = []
        suit_list = ["hearts", "spades", "diamonds", "clubs"]
        numeral_list = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        for suit in suit_list:
            for value in range(1, 14):
                i = value - 1
                numeral = numeral_list[i]
                self.deck.append(Card(value, numeral, suit))
    def shuffle(self):
        random.shuffle(self.deck)
        return self
    def deal(self, Player):
        card = self.deck.pop()
        Player.hand.append(card)
        return self
    def deal_show(self, Player):
        card = self.deck.pop()
        Player.hand.append(card)
        print("You drew:", end=" ")
        card.show()
        return self
    def show(self):
        print("\n", "*"*30, self.name, "*"*30)
        for card in self.deck:
            card.show()
        return self

class Game:
    def __init__(self):
        self.players = []
    def start_game(self):
        name = input("\n Player 1, enter your name: ")
        player1 = Player(name, 1)
        player2 = Player("the Jack", 2)
        player3 = Player("the Queen", 3)
        player4 = Player("the King", 4)
        self.players.append(player1)
        self.players.append(player2)
        self.players.append(player3)
        self.players.append(player4)
        return self
    def show(self):
        self.players[0].sort_cards().remove_sets().show_all()
        for i in range(1, len(self.players)):
            self.players[i].sort_cards().remove_sets().show_some()
        return self

def active_players(game):
    count = 0
    for player in game.players:
        if len(player.hand) > 0:
            count += 1
    return count

def play_game():
    print("\n", "Welcome to GO FISH!")
    deck = Deck("Game Deck")
    deck.shuffle()
    game = Game()
    game.start_game()
    for i in range(7):
        for j in range(len(game.players)):
            deck.deal(game.players[j])
    game.show()
    print("\n", "There are", len(deck.deck), "more cards in the deck.")

    # determine while loop
    active_players_flag = True
    while len(deck.deck) > 0 and active_players_flag:
        # human player's turn
        go_fish_flag = False
        while not go_fish_flag and active_players_flag:
            if len(game.players[0].hand) > 0:
                opponent_choices = [2, 3, 4]
                opponent_flag = False
                while not opponent_flag:
                    result = input(f"\n {game.players[0].name}, from whom would you like to ask a card? (enter the player's number)   ")
                    valid_result = result.isdigit()
                    if valid_result:
                        opponent = int(result)
                        for i in range(len(opponent_choices)):
                            if opponent == opponent_choices[i]:
                                for j in range(len(game.players)):
                                    if opponent == game.players[j].position:
                                        opponent_player = game.players[j]
                                        if len(opponent_player.hand) == 0:
                                            print(f"{opponent_player.name} does not have any cards.", end=" ")
                                        else:
                                            opponent_flag = True
                        if opponent_flag:
                            print(f"You have chosen to ask {opponent_player.name} for a card.")
                        else:
                            print("Invalid selection. Please choose again.")
                    else:
                        print("Invalid selection. Please choose again. From whom would you like to ask a card? (enter the player's number) ")
                request_choices = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
                request_flag = False
                while not request_flag:
                    request = input(f"\n {game.players[0].name}, which card would you like? (Press 'A' for Ace, '2' for 2, '3' for 3 ... 'J' for Jack, 'Q' for Queen, 'K' for King)   ")
                    request = request.upper()
                    for i in range(len(request_choices)):
                        if request == request_choices[i]:
                            for j in range(len(game.players[0].hand)):
                                if request == game.players[0].hand[j].numeral:
                                    request_flag = True
                            if not request_flag:
                                print("You must choose a card value that you currently hold in your hand.", end=" ")
                    if request_flag:
                        print(f"You have asked for {request}'s.")
                    else:
                        print("Invalid selection. Please choose again.")
                flag = True
                requested_cards = []
                while flag and len(opponent_player.hand) > 0:
                    flag = False
                    for i in range(len(opponent_player.hand)):
                        if request == opponent_player.hand[i].numeral:
                            requested_cards.append(opponent_player.hand[i])
                            for j in range(i, len(opponent_player.hand)-1):
                                opponent_player.hand[j] = opponent_player.hand[j+1]
                            opponent_player.hand.pop()
                            flag = True
                            break
                if len(requested_cards) == 1:
                    print("\n", f"{opponent_player.name} has {len(requested_cards)} {request}.")
                    requested_cards[0].show()
                    game.players[0].hand.append(requested_cards[0])
                elif len(requested_cards) > 1:
                    print("\n", f"{opponent_player.name} has {len(requested_cards)} {request}'s.")
                    for i in range(len(requested_cards)):
                        requested_cards[i].show()
                        game.players[0].hand.append(requested_cards[i])
                else:
                    print("\n", f"{opponent_player.name} does not have any {request}'s. GO FISH!")
                    deck.deal_show(game.players[0])
                    print("\n", "There are", len(deck.deck), "more cards in the deck.")
                    go_fish_flag = True
                game.show()
                count = active_players(game)
                if count < 2:
                    active_players_flag = False
            else:
                print("\n", "You have no cards in your hand. Your turn is skipped.")
                go_fish_flag = True
            print("\n")

        # computers's turns
        for position in range(2, len(game.players)+1):
            print("$"*90)
            ready = input("Press enter to continue with the game.")
            for i in range(len(game.players)):
                if position == game.players[i].position:
                    current_player = game.players[i]
            print("current player:", current_player.name)
            go_fish_flag = False
            while not go_fish_flag and active_players_flag:
                if len(current_player.hand) > 0:
                    opponent_choices = []
                    for opponent_position in range(1, len(game.players)+1):
                        if opponent_position != current_player.position:
                            opponent_choices.append(opponent_position)
                    opponent_flag = False
                    while not opponent_flag:
                        rand_num = random.randint(0,len(opponent_choices)-1)
                        opponent = opponent_choices[rand_num]
                        for i in range(len(game.players)):
                            if opponent == game.players[i].position:
                                opponent_player = game.players[i]
                        if len(opponent_player.hand) > 0:
                            opponent_flag = True
                            print("opponent:", opponent_player.name)
                    request_choices = ["A", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
                    request_flag = False
                    while not request_flag:
                        rand_num = random.randint(0, len(request_choices)-1)
                        request = request_choices[rand_num]
                        for i in range(len(current_player.hand)):
                            if request == current_player.hand[i].numeral:
                                request_flag = True
                        if request_flag:
                            print("requested card:", request)
                    flag = True
                    requested_cards = []
                    while flag and len(opponent_player.hand) > 0:
                        flag = False
                        for i in range(len(opponent_player.hand)):
                            if request == opponent_player.hand[i].numeral:
                                requested_cards.append(opponent_player.hand[i])
                                for j in range(i, len(opponent_player.hand)-1):
                                    opponent_player.hand[j] = opponent_player.hand[j+1]
                                opponent_player.hand.pop()
                                flag = True
                                break
                    if len(requested_cards) == 1:
                        print(f"{opponent_player.name} has {len(requested_cards)} {request}.")
                        requested_cards[0].show()
                        current_player.hand.append(requested_cards[0])
                    elif len(requested_cards) > 1:
                        print(f"{opponent_player.name} has {len(requested_cards)} {request}'s.")
                        for i in range(len(requested_cards)):
                            requested_cards[i].show()
                            current_player.hand.append(requested_cards[i])
                    else:
                        print(f"{opponent_player.name} does not have any {request}'s. GO FISH!")
                        deck.deal(current_player)
                        go_fish_flag = True
                        print("\n", "There are", len(deck.deck), "more cards in the deck.")
                    game.show()
                    count = active_players(game)
                    if count < 2:
                        active_players_flag = False
                    if not go_fish_flag and active_players_flag:
                        print("*"*30)
                else:
                    print(f"{current_player.name} does not have any cards. Skip turn!")
                    go_fish_flag = True
                print("\n")
    # declare winner
    game.players.sort(key=lambda player: player.points, reverse=True)
    winners = [game.players[0]]
    max_points = game.players[0].points
    for i in range(1, len(game.players)):
        if game.players[i].points >= max_points:
            max_points = game.players[i].points
            winners.append(game.players[i])
    if len(winners) == 1:
        print(f"The winner is {winners[0].name}!")
    else:
        print("The winners are:")
        for i in range(len(winners)):
            print(f"{winners[i].name}!")
    for i in range(len(game.players)):
        print("Name:", game.players[i].name, "*"*10, "Points:", game.players[i].points)
play_game()
