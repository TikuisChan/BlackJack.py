import random


class Deck(object):
    # store the cards in a static class, with D as diamonds, C as clubs, S as spades and H as hearts
    full_deck = ['\u2666 A', '\u2666 2', '\u2666 3', '\u2666 4', '\u2666 5', '\u2666 6', '\u2666 7', '\u2666 8', '\u2666 9', '\u2666 10', '\u2666 J', '\u2666 Q', '\u2666 K',
                 '\u2663 A', '\u2663 2', '\u2663 3', '\u2663 4', '\u2663 5', '\u2663 6', '\u2663 7', '\u2663 8', '\u2663 9', '\u2663 10', '\u2663 J', '\u2663 Q', '\u2663 K',
                 '\u2660 A', '\u2660 2', '\u2660 3', '\u2660 4', '\u2660 5', '\u2660 6', '\u2660 7', '\u2660 8', '\u2660 9', '\u2660 10', '\u2660 J', '\u2660 Q', '\u2660 K',
                 '\u2665 A', '\u2665 2', '\u2665 3', '\u2665 4', '\u2665 5', '\u2665 6', '\u2665 7', '\u2665 8', '\u2665 9', '\u2665 10', '\u2665 J', '\u2665 Q', '\u2665 K']
    # full_deck = ['B 6', 'A 6', 'C 6', 'D 6', 'E 6', 'F 6', 'G 6', 'H 6', 'I 6', 'J 6', 'K 6', 'L 6', 'M 6',
    #              'Z 6', 'Y 6', 'x 6', 'w 6', 'V 6', 'U 6', 'T 6', 'S 6', 'R 6', 'Q 6', 'P 6', 'O 6', 'N 6']
    deck = []

    def __init__(self, num_deck):
        self.num_deck = num_deck
        Deck.deck = Deck.full_deck * self.num_deck
        random.shuffle(Deck.deck)

    @staticmethod
    def add_deck():
        add = Deck.full_deck
        random.shuffle(add)
        Deck.deck += add
        print('A new deck is added')


class Hand(object):
    def __init__(self):
        self.hand_card = []
        self.suit = []
        self.card = []
        self.pts = []

    def draw_card(self, n):
        if len(Deck.deck) <= n:
            Deck.add_deck()
        for a in range(n):
            self.hand_card.append(Deck.deck.pop())

    def read_card(self):
        cal_points = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                      '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
        self.card.clear()
        self.pts.clear()
        self.suit.clear()
        for card in self.hand_card:
            self.suit.append(card[:1])
            self.card.append(card[2:])
            self.pts.append(cal_points[card[2:]])
        return self.suit, self.card, self.pts

    def check_pairs(self):
        if len(self.card) < 2:
            return False
        num_pairs = 0
        for n in range(len(self.card)):
            for m in range(n+1, len(self.card)):
                if self.card[n] == self.card[m]:
                    num_pairs += 1
        return num_pairs
