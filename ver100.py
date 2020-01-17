import random


class Deck(object):
    # store the cards in a static class
    n = 4
    full_deck = {'A': n, '2': n, '3': n, '4': n,
                 '5': n, '6': n, '7': n, '8': n,
                 '9': n, '10': n, 'J': n, 'Q': n,
                 'K': n}


class Player(object):
    def __init__(self):
        self.hands = {}
        self.point = 0

    def hit(self):
        # draw, num_card = 'A', self.full_deck['A']
        draw, num_card = random.choice(list(Deck.full_deck.items()))
        if draw in self.hands.keys():   # update cards in player's hand
            self.hands[draw] += 1
        else:
            self.hands[draw] = 1
        if num_card == 1:   # delete the card from the full deck
            Deck.full_deck.pop(draw)
        else:
            Deck.full_deck[draw] -= 1
        return draw

    def count(self):
        self.point = 0
        bust = False
        cal_points = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                      '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                      'J': 10, 'Q': 10, 'K': 10}
        # count point without the As
        for n in self.hands.keys():
            if n in cal_points and n != 'A':
                self.point += cal_points[n] * self.hands[n]

        # handling the As
        if 'A' in self.hands:
            if self.point < 11:
                self.point += 11 + (self.hands['A']-1)
            elif self.point >= 11:
                self.point += self.hands['A']

        if self.point > 21:
            bust = True
        return bust


class BlackJack(object):
    def __init__(self):
        # create dealer and player(s)
        self.Dealer = Player()
        self.Player1 = Player()
        # deal cards to player(s) and show one card of dealer

    def start(self):
        self.Player1.hit()
        self.Player1.hit()
        self.Player1.bust = self.Player1.count()
        self.Dealer.hit()
        print('Your hands: ')
        print(self.Player1.hands)
        print('Your point: %d' % self.Player1.point)
        print("Dealer's hand: ")
        print(self.Dealer.hands)
        while True:
            usr_choice = input('Do you want to (H)it or (S)tand?')
            if usr_choice == 'H':
                self.Player1.hit()
                self.Player1.bust = self.Player1.count()
                print('Your hands: ')
                print(self.Player1.hands)
                print('Your point: %d' % self.Player1.point)
                if self.Player1.bust is True:
                    print('Bust!')
                    return
            elif usr_choice == 'S':
                return
            else:
                print('Wrong input, please choose again: (H)it or (S)tand')

    def dealer_turn(self):
        self.Dealer.hit()
        self.Dealer.bust = self.Dealer.count()
        print("Dealer's hand: ")
        print(self.Dealer.hands)
        while self.Dealer.point < 17:
            self.Dealer.hit()
            self.Dealer.bust = self.Dealer.count()
            print("Dealer's hand: ")
            print(self.Dealer.hands)

    def winner(self):
        self.Dealer.bust = self.Dealer.count()
        self.Player1.bust = self.Player1.count()
        print('Your point: %d' % self.Player1.point)
        print("Dealer's point: %d" % self.Dealer.point)
        if self.Dealer.bust is True and self.Player1.bust is False:
            print('Dealer Bust! You win')
        elif self.Dealer.bust is False and self.Player1.bust is True:
            print('You busted! Sorry...')
        elif self.Dealer.bust == self.Player1.bust is True:
            print('Draw! Super')
        else:
            if 21 >= self.Player1.point > self.Dealer.point:
                print('Congrad! You win!')
            elif 21 >= self.Dealer.point > self.Player1.point:
                print('Oh no! You lose')
            elif self.Player1.point == self.Dealer.point:
                print('Draw! Super!')


NewGame = BlackJack()
NewGame.start()
NewGame.dealer_turn()
NewGame.winner()
