import random

class hand:
    def __init__(self, cards = [], deck = None):
        self.cards = []
        if cards and deck:
            for card in cards:
                if card in deck.cards:
                    self.cards.append(card)
                    deck.cards.remove(card)
                else:
                    print(card.render(), "not in deck.")
    def draw(self, deck):
        """
        Draws cards from given deck.
        """
        for _ in range(2):
            chosen_index = random.randint(0, len(deck.cards)-1)
            self.cards.append(deck.cards.pop(chosen_index))
    def return_cards(self, deck):
        """
        Returns cards to deck.
        """
        while len(self.cards) > 0:
            deck.cards.append(self.cards.pop(0))

class card:
    def __init__(self, suit, value):
        """
        Base card unit, containing suit and value.
        """
        self.suit = suit
        self.value = value
    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value
    def render(self):
        """
        String rendering of a card, eg: AC = ace of clubs, 9H = nine of hearts
        """
        valtext = ""
        suittext = self.suit
        if self.value < 11:
            valtext = str(self.value)
        else:
            facecards = {11:"J", 12:"Q", 13:"K", 14:"A"}
            valtext = facecards[self.value]
        return valtext+"-"+suittext

class deck:
    def __init__(self):
        """
        Deck unit, used for possible cards opponent may have
        """
        self.cards = []
        self.add_cards()
    def add_cards(self):
        """
        Populates the deck with cards.
        """
        suits = ["H", "D", "C", "S"]
        for suit in range(4):
            for val in range(2, 15):
                self.cards.append(card(suits[suit], val))

class field:
    def __init__(self):
        self.cards = []
    def draw_determined(self, deck, card):
        if card in deck.cards:
            self.cards.append(card)
            deck.cards.remove(card)
        else:
            print(card.render(), "not in deck.")
    def draw(self, deck):
        """
        Draws cards from given deck.
        """
        if len(self.cards) < 4:
            chosen_index = random.randint(0, len(deck.cards)-1)
            self.cards.append(deck.cards.pop(chosen_index))
        else:
            for _ in range(2):
                chosen_index = random.randint(0, len(deck.cards)-1)
                self.cards.append(deck.cards.pop(chosen_index))
    def return_cards(self, deck):
        """
        Returns cards to deck.
        """
        while len(self.cards) > 0:
            deck.cards.append(self.cards.pop(0))