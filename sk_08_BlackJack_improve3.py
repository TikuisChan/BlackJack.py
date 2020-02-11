#!/usr/bin/env/ python3.7

import sk_07_PokerBasic as pb


class Player(object):
    def __init__(self, chips):
        self.hands_obj = [pb.Hand()]
        self.blackjack = [False]
        self.bust = [False]
        self.points = []
        self.chips = chips

    def ini_step(self, index):
        # check if hands[index] exist & having 2 cards
        while len(self.hands_obj[index].hand_card) < 2:
            self.hands_obj[index].draw_card(1)
        # draw cards until 2 cards in hands[index]
        suit, card, pts = self.hands_obj[index].read_card()
        if card[0] == card[1]:
            print('Initial hand: ' + str(self.hands_obj[index].hand_card))
            usr_split = input('Do you want to split? (y/n)')
            if usr_split.lower() == 'y':
                self.split(index)
            else:
                self.points.insert(index, self.cal_point(index))
        else:
            self.points.insert(index, self.cal_point(index))

    def play(self, index):
        while not self.bust[index] and not self.blackjack[index]:
            print('Your ' + str(index+1) + ' hand is: ' + str(self.hands_obj[index].hand_card))
            usr_choice = input('Do you want to: (h)it, (s)tand or (d)ouble down?')
            if usr_choice.lower() == 'h':
                self.hit(index)
            elif usr_choice.lower() == 's':
                self.cal_point(index)
                return
            elif usr_choice.lower() == 'd':
                self.hit(index)
                return
            else:
                print('wrong input :(')

    def cal_point(self, index):
        pts = 0
        cal_points = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                      '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
        for n in self.hands_obj[index].card:
            if n != 'A':
                pts += cal_points[n]
        # handling the As
        if 'A' in self.hands_obj[index].card:
            num_a = self.hands_obj[index].card.count('A')
            if pts + num_a + 10 <= 21:
                pts += 11 + (num_a-1)
            else:
                pts += num_a
        # Blackjack
        if len(self.hands_obj[index].card) == 2 and pts == 21:
            self.blackjack[index] = True
            print('blackjack!')
        # Bust
        if pts > 21:
            self.bust[index] = True
            print('bust!')

        print(str(self.hands_obj[index].hand_card) + ' total point is: ' + str(pts))
        return pts

    def hit(self, index):
        self.hands_obj[index].draw_card(1)
        self.hands_obj[index].read_card()
        self.points[index] = self.cal_point(index)

    def stand(self, index):
        pass

    def double(self, index):
        self.hands_obj[index].draw_card(1)
        self.hands_obj[index].read_card()
        self.points[index] = self.cal_point(index)

    def split(self, index):
        split_hand = pb.Hand()
        self.bust.insert(index+1, False)
        self.blackjack.insert(index+1, False)
        self.points.insert(index+1, 0)
        self.hands_obj.insert(index+1, split_hand)
        self.hands_obj[index + 1].hand_card.append(self.hands_obj[index].hand_card.pop())
        self.ini_step(index)

    def clear(self):
        self.hands_obj = [pb.Hand()]
        self.blackjack = [False]
        self.bust = [False]
        self.points = [0]


class Dealer(Player):
    # no split, hit until 17
    def ini_step(self, index):
        self.clear()
        # check if hands[index] exist & having 2 cards
        while len(self.hands_obj[index].hand_card) < 2:
            self.hands_obj[index].draw_card(1)
        # draw cards until 2 cards in hands[index]
        self.hands_obj[index].read_card()
        self.points.insert(index, self.cal_point(index))

    def play(self, index, target=17):
        print(self.hands_obj[index].hand_card)
        while self.points[index] < target:
            print('hit!')
            self.hit(index)
        if not self.bust[index] and not self.blackjack[index]:
            print('stand')


class BlackJack(object):
    # initial: create player (Dealer + 3 AIs), create deck
    def __init__(self):
        self.Dealer = Dealer(10000)
        self.Player1 = Dealer(10000)
        self.Player2 = Dealer(10000)
        self.Player3 = Dealer(10000)
        self.Player4 = Player(10000)
#        self.players = [self.Player1, self.Player4, self.Dealer]
        self.players = [self.Player1, self.Player2, self.Player3, self.Player4, self.Dealer]
        self.deck = pb.Deck(1)

    def start_loop(self):
        # initial position, every player takes 2 cards, check split condition
        for n, player in enumerate(self.players, start=1):
            player.clear()
            if player == self.Dealer:
                print("Dealer's initial hand: ", end='')
            else:
                print('Player ' + str(n) + "'s initial hand: ", end='')
            a = 0
            while a < len(player.hands_obj):
                player.ini_step(a)
                a += 1

    def main_loop(self):
        # main game stage, hit, double down or stand
        for n, player in enumerate(self.players, start=1):
            if player == self.Dealer:
                print("Dealer's turn: ")
            else:
                print('Player ' + str(n) + "'s turn: ")
            for index, hand in enumerate(player.hands_obj):
                player.play(index)

    def report_chips(self):
        # conclude game according to players' points
        print('-' * 50)
        print('Game conclude:')
        for n, player in enumerate(self.players, start=1):
            if player == self.Dealer:
                continue
            for m, check_bust in enumerate(player.bust):
                if check_bust:
                    print('Player %d bust.' % n)
                    continue
            for m, check_bj in enumerate(player.blackjack):
                if check_bj and self.Dealer.blackjack[0]:
                    print('Player %d push (blackjack)' % n)
                elif check_bj and not self.Dealer.blackjack[0]:
                    print('Player %d blackjack! congrad!' % n)
                elif not check_bj and self.Dealer.blackjack[0]:
                    print("Dealer's blackjack, Player %d lose" % n)
                else:
                    if self.Dealer.points[0] < player.points[m] <= 21:
                        print('Player %d win a hand!' % n)
                    elif player.points[m] < self.Dealer.points[0] <= 21:
                        print('Player %d lose a hand...' % n)
                    elif player.points[m] == self.Dealer.points[0] <= 21:
                        print('Player %d push (same point)' % n)
                    elif self.Dealer.bust[0] and player.points[m] <= 21:
                        print('Dealer bust, Player %d win!' % n)
        # check: if the chips of player is not enough, ask player to add chips


New_game = BlackJack()
while True:
    New_game.start_loop()
    New_game.main_loop()
    New_game.report_chips()
    usr_con = input('Continue? (y/n)')
    if usr_con.lower() == 'n':
        break
