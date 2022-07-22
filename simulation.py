from evaluate import victor
import infrastructure as infr
import random

class bot_iteration:
    def __init__(self, chips=100, depth = 1000, hand_depth = 1000, loss_aversion = 1.075, heat = 0):
        """
        chips are current chips
        depth are amount of field simulations made to judge hand strength
        hand depth are number of hands against each field
        loss aversion is bias toward conservative play
        heat is tolerance of randomness, to be implemented
        """
        self.chips = chips
        self.depth = depth
        self.hand_depth = hand_depth
        self.loss_aversion = loss_aversion
        self.heat = heat
        self.last_bet = 0
        self.last_win_pct = -1
    
    def judge_position(self, hand, field, deck):
        """
        Gives win percentage off of random fields, hands.  In the future will include opponent's betting info inshallah.
        """
        normal_cards = []
        for card in deck.cards:
            normal_cards.append(card)
        practice_field = infr.field()
        for card in field.cards:
            practice_field.cards.append(card)
        results = {"W": 0, "D": 0, "L":0}
        for i in range(self.depth):
            while len(practice_field.cards) < 5:
                practice_field.draw(deck)
            for j in range(self.hand_depth):
                otherhand = infr.hand()
                otherhand.draw(deck)
                results[victor(practice_field, hand, otherhand)]+= 1
                otherhand.return_cards(deck)
            deck.cards = []
            for card in normal_cards:
                deck.cards.append(card)
            practice_field.cards = []
            for card in field.cards:
                practice_field.cards.append(card)
            #print(results, len(deck.cards),[card.render() for card in field.cards], [card.render() for card in practice_field.cards])
        self.last_win_pct = results["W"]/(results["W"]+results["L"])
        return results["W"]/(results["W"]+results["L"])

    def judge_bet(self, attempts, bet, win_pct):
        """
        Flips coin in line with win_percent and adjusts expected losses with loss aversion."""
        wins = 0
        losses = 0
        for i in range(attempts):
            if random.random() < win_pct:
                wins += bet
            else:
                losses += bet
        return (wins - losses**self.loss_aversion)/attempts
    
    def generate_bet(self, win_pct, ante = -1):
        """
        Decides bet
        """
        best_bet = 0
        best_winning = ante
        for bet in range(1, self.chips+1):
            judgement = self.judge_bet(self.depth // 2, bet, win_pct)
            if judgement > best_winning:
                best_winning = judgement
                best_bet = bet
        return best_bet

    def play(self, hand, field, deck):
        return self.generate_bet(self.judge_position(hand, field, deck))

    def render_bet(self, bet):
        self.chips -= bet
        self.last_bet += bet
    
    def respond_to_raise(self,  response):
        judgement = self.judge_bet(self.depth, response, self.last_win_pct)
        if judgement > -1*self.last_bet:
            print("Call.", judgement)
            self.chips -= (response-self.last_bet)
        else:
            print("Fold.", judgement)
        