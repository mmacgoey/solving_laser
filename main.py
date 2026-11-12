import random

numbers = range(2,15)
suits = ["hearts", "diamonds", "spades", "clubs"]
num_players = 4

class Card:

     # defines a card by its numerical value and suit
     def __init__(self, number : int, suit : str):

          self.number = number
          self.suit = suit
          self.is_seen = False
          self.is_passed = False
          self.is_scoring = False

          self.is_black = True if ((self.suit == "clubs") or (self.suit == "spades")) else False
          self.is_black_ten = True if (self.is_black and self.number == 10) else False
          self.is_laserable = True if (self.number > 10 and self.is_black) else False
          self.is_joker = True if (self.suit == "joker") else False

     def get_card_info(self):

          return {
          
                         "number" : self.number,
                         "suit" : self.suit,
                         "seen?" : self.is_seen,
                         "passed?" : self.is_passed,
                         "scoring?" : self.is_scoring,
                         
                    }

class Deck:

     # creates the deck of cards
     def __init__(self):

          self.cards = []

          for s in suits:
               for n in numbers:

                    self.cards.append(Card(n, s))

          # add in the joker
          self.cards.append(Card(0, "joker"))

     # removes a card from the deck
     def remove_cards(self, card : Card):

          if card.isin(self.cards):

               self.cards.remove(card)

          else:

               print("card not in deck!")

     # deal a hand of three random cards from the deck into a hand
     def deal_hand(self):

          a_hand = random.sample(self.cards, 3)

          for card in a_hand:
               self.cards.remove(card)

          return Player(a_hand)

class Player:

     # deals a hand to the player
     def __init__(self, cards):

          self.cards = cards
          self.is_immune = False
          self.round_score = 0
          self.overall_score = 0

     def identify_hand(self):

          self.card_1, self.card_2, self.card_3 = self.cards
          return self.card_1.get_card_info(), self.card_2.get_card_info(), self.card_3.get_card_info()

     # look at two of the three cards in hand, choosing randomly
     def look(self):

          revealed = random.sample(self.cards, 2)

          for c in revealed:
               c.is_seen = True

# choose a random card from the remaining deck to be the centre card 
def choose_centre_card(deck : Deck):

     return random.choice(deck.cards)

# def create_players(players):

#      for i in range(num_players):
#           players.append(Player())

def pass_card(player_1 : Player, player_2 : Player, card : Card):

     player_2.cards.append(card)
     player_1.cards.remove(card)
     card.passed = True

def choose_scoring_cards(player : Player):

     # randomly choose to play one or two scoring cards
     num_scoring_cards = random.choice([1,2])

     scoring_cards = random.sample(player.cards, num_scoring_cards)

     for card in scoring_cards:

          card.is_scoring = True

def apply_scoring_rules(player : Player, scoring_cards, auxiliary_cards):

     score = 0
     auxiliary_score = 0

     for i, cards in enumerate([scoring_cards, auxiliary_cards]):

          card_1, card_2 = cards

          if card_1.is_laserable and card_2.is_laserable:

               s = -10
               player.is_immune = True

          elif card_1.is_black_ten and card_2.is_black_ten:

               s = -100 # FIGURE OUT WHAT THIS ACTUALLY IS

          elif card_1.is_black_ten:

               s = 10 - card_2.number

          elif card_2.is_black_ten:

               s = 10 - card_1.number

          else:
               
               s = card_1.number + card_2.number

          if i == 0: score = s
          else: auxiliary_score = s          

     # print("BEFORE AUXILIARY CHECK")
     # print(score, auxiliary_score)

     if auxiliary_score < score:

          score -= max([c.number for c in scoring_cards])

     # print("POST AUXILIARY CHECK")
     # print(score, auxiliary_score)

     player.round_score = score

def determine_scoring(players, centre_card):

     # first pass
     for player in players:

          scoring_cards = [card for card in player.cards if card.is_scoring]
          auxiliary_cards = [card for card in player.cards if not card.is_scoring]

          if len(scoring_cards) == 1:
               scoring_cards.append(centre_card)
          else:
               auxiliary_cards.append(centre_card)

          apply_scoring_rules(player, scoring_cards, auxiliary_cards)

     player_scores = [p.round_score for p in players]

     lowest_player = next(p for p, s in zip(players, player_scores) if s == min(player_scores))
     lowest_player.round_score += 25

     final_player_scores = [p.round_score for p in players]

     print(final_player_scores)

     for i, p in enumerate(players):

          p.overall_score += final_player_scores[i]


def one_round():

     players = []
     deck = Deck()

     for player in range(num_players):

          p = deck.deal_hand()
          players.append(p)
          p.look()

     for i in range(num_players):

          # current player's turn
          p1 = players[i]

          # next player, if last player loop back to the first
          p2 = players[i+1] if not (i == num_players - 1) else players[0]

          # randomly select a card to pass along
          card_to_pass = random.choice(p1.cards)

          pass_card(p1, p2, card_to_pass)

     for p in players:
          print(p.identify_hand())

     deck.deal_hand()

     centre_card = choose_centre_card(deck)

     for player in players:
          choose_scoring_cards(player)

     determine_scoring(players, centre_card)

     return players

playing = True
rounds = 0

while playing:
     
     rounds += 1

     players = one_round()

     overall_scores = [p.overall_score for p in players]

     print("round: " + str(rounds))
     print("scores: " + str(overall_scores))
     
     if min([p.overall_score for p in players]) <= -100:
          print("someone won!")
          break
