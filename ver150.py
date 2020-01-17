"""
SK Black Jack version 1.50
** Formal rules of Black Jack
** 1 - 4 players vs dealer
** Player can now choose Hit, Stand or Split (if possible)
- No betting
** Change of drawing system (from 1/13 to 1/52 for closer to reality), can now adjust the number of decks in a game
** Can continue playing after a game
"""
import random


class Deck(object):
    # store the cards in a static class, with D as diamonds, C as clubs, S as spades and H as hearts
    # full_deck = ['D A', 'D 2', 'D 3', 'D 4', 'D 5', 'D 6', 'D 7', 'D 8', 'D 9', 'D 10', 'D J', 'D Q', 'D K',
    #              'C A', 'C 2', 'C 3', 'C 4', 'C 5', 'C 6', 'C 7', 'C 8', 'C 9', 'C 10', 'C J', 'C Q', 'C K',
    #              'S A', 'S 2', 'S 3', 'S 4', 'S 5', 'S 6', 'S 7', 'S 8', 'S 9', 'S 10', 'S J', 'S Q', 'S K',
    #              'H A', 'H 2', 'H 3', 'H 4', 'H 5', 'H 6', 'H 7', 'H 8', 'H 9', 'H 10', 'H J', 'H Q', 'H K']
    full_deck = ['B 6', 'A 6', 'C 6', 'D 6', 'E 6', 'F 6', 'G 6', 'H 6', 'I 6', 'J 6', 'K 6', 'L 6', 'M 6',
                 'Z 6', 'Y 6', 'x 6', 'w 6', 'V 6', 'U 6', 'T 6', 'S 6', 'R 6', 'Q 6', 'P 6', 'O 6', 'N 6']


class Player(object):
    def __init__(self):
        self.hands = []
        self.point = 0
        self.blackjack = False
        self.bust = False
        self.split_chance = False

    def clr_hand(self):
        self.hands.clear()
        self.point = 0
        self.blackjack = False
        self.bust = False

    def hit(self):
        draw = random.choice(Deck.full_deck)    # randomly remove a card from full_deck
        Deck.full_deck.remove(draw)
        self.hands.append(draw)    # update cards in player's hand
        self.__count__()
        return draw

    def __count__(self):
        self.point = 0
        cal_points = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                      '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
        # remove suits in hands for point counting and store at hand_pt
        hand_pt = []
        for card in self.hands:
            card_pt = card.split(' ', 2)
            hand_pt.append(card_pt[1])
        if len(hand_pt) == 2 and hand_pt[0] == hand_pt[1]:    # condition for split
            self.split_chance = True
        # count point (using hand_pt) without the As
        for n in hand_pt:
            if n != 'A':
                self.point += cal_points[n]
        # handling the As
        if 'A' in hand_pt:
            num_a = hand_pt.count('A')
            if self.point < 11:
                self.point += 11 + (num_a-1)
            elif self.point >= 11:
                self.point += num_a
        # BlackJack
        if len(hand_pt) == 2 and self.point == 21:
            self.blackjack = True
        # Bust
        if self.point > 21:
            self.bust = True


class BlackJack(object):
    def __init__(self, deck_num, player_num=4):
        self.Dealer = Player()
        self.player_num = player_num
        self.create_players()
        self.n = deck_num
        Deck.full_deck = Deck.full_deck * self.n    # control the number of decks in use

    def create_players(self):
        self.players = [Player() for i in range(self.player_num)]

    def first_deal(self):
        self.Dealer.clr_hand()
        self.Dealer.hit()
        print("Dealer's hand: %s" % ' ,'.join(self.Dealer.hands))
        for n, i in enumerate(self.players, start=1):    # first round of dealing
            i.clr_hand()
            i.hit()
            print("Player %d : %s" % (n, ' ,'.join(i.hands)))

    def game(self):
        for n, i in enumerate(self.players, start=1):
            print(i.hands)
            i.hit()
            print("Player %d hand: %s" % (n, ' ,'.join(i.hands)))
            print('Player %d point: %d' % (n, i.point))
            if i.blackjack:
                print('BlackJack!!')
                continue
            if i.split_chance:
                usr_input = input('Do you want to split? (y/n)')
                if usr_input.lower() == 'y':
                    self.split(n-1)
                    continue
                elif usr_input.lower() == 'n':
                    i.split_chance = False
            self.player_turn(n, i)
            continue

    @staticmethod
    def player_turn(n, i):
            turn = True
            while turn is True:
                usr_choice = input('Do you want to (H)it or (S)tand?')
                if usr_choice.upper() == 'H':
                    i.hit()
                    print("Player %d hand: %s" % (n, ' ,'.join(i.hands)))
                    print('Player %d point: %d' % (n, i.point))
                    if i.bust is True:
                        print('Bust!')
                        turn = False
                elif usr_choice.upper() == 'S':
                    turn = False
                else:
                    print('Wrong input, please choose again: (H)it or (S)tand')

    def dealer_turn(self):
        self.Dealer.hit()
        print("Dealer's hand: %s" % ' ,'.join(self.Dealer.hands))
        while self.Dealer.point < 17:
            print('Dealer hit')
            self.Dealer.hit()
            print("Dealer's hand: %s" % ' ,'.join(self.Dealer.hands))

    def winner(self):
        print("Dealer's point: %d" % self.Dealer.point)
        for n, i in enumerate(self.players, start=1):
            if i.split_chance:
                continue
            print('Player %d have: %d points' % (n, i.point))
            if i.bust:
                print('Bust! You (Player %d) lose!' % n)
            elif self.Dealer.bust is True and i.bust is False:
                print('Dealer Bust! You win!')
            elif self.Dealer.blackjack == i.blackjack is True:
                print('Tie!')
            elif self.Dealer.blackjack is True and i.blackjack is False:
                print("Dealer's blackjack, you loss")
            elif self.Dealer.blackjack is False and i.blackjack is True:
                print('Player %d  win!' % n)
            else:
                if 21 >= i.point > self.Dealer.point:
                    print('Player %d  win!' % n)
                elif 21 >= self.Dealer.point > i.point:
                    print('Oh no! Player %d  lose' % n)
                elif i.point == self.Dealer.point:
                    print('Tie!')

    def split(self, n):
        [a, b] = self.players[n].hands
        self.splita = Player()
        self.splitb = Player()
        self.players.insert(n+1, self.splita)
        self.players.insert(n+1, self.splitb)
        self.players[n+1].clr_hand()
        self.players[n+2].clr_hand()
        self.players[n+1].hands.append(a)
        self.players[n+2].hands.append(b)


NewGame = BlackJack(2, 1)
while True:
    NewGame.first_deal()
    NewGame.game()
    NewGame.dealer_turn()
    NewGame.winner()
    print('There are %d cards left.' % len(Deck.full_deck))
    exit_game = input('One more game? (To exit, please input x)')
    if exit_game == 'x':
        break
