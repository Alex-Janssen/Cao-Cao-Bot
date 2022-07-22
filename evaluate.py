import infrastructure as infr

# Syntax for evaluation results
# Tuple, with first value being a code for the type of hand, second for the value of that type
# First value meanings
# 0, high card 2nd
# 1, two of a kind of 2nd
# 2, two pair with highest value 2nd
# 3, 3 of a kind 2nd
# 4, straight with low 2nd
# 5, flush with high 2nd
# 6, full house with 2nd representing the 3
# 7, four of a kind with 2nd
# 8, straight flush with low 2nd (which includes royal flush)

def find_best_hand(hand, field):
    """
    Returns the optimal grouping of five cards with field and hand in tact.
    """
    cards = hand.cards + field.cards
    cards.sort(key=lambda card : card.value*-1) #reverse so program can terminate early
    #variable definitions
    maxvals = (0, cards[0].value) #evaluation to be returned
    suits = {"H": [0,0],"D": [0,0], "S": [0,0],"C":[0,0] } #Suit, count of suit, highest
    matches = {2: [0, None], 3: [0, None], 4: [0, None]} #for pairs, three and fours of a kind
    last_seen = infr.card("NONE", -2) #for comparisons
    sequential_in_a_row = 0 #for straights
    sequential_in_a_row_same_suit = 0 #straight flush
    straight_flush_memory = ["NONE", -1, -1] #suit, length, and last value of candidate straight flush, only used if 
    same_in_a_row = 0 #for keeping track of pairs
    straight = None #if a straight is found
    for card in cards:
        suits[card.suit][0] += 1
        if suits[card.suit][1] == 0:
            suits[card.suit][1] = card.value 
        if card.value == last_seen.value-1:
            #processing pairs
            if same_in_a_row in matches.keys():
                matches[same_in_a_row][0] += 1
                if matches[same_in_a_row][1] == None:
                    matches[same_in_a_row][1] = last_seen.value
            same_in_a_row = 1
            #processing sequentials
            sequential_in_a_row += 1
            if card.suit == last_seen.suit:
                sequential_in_a_row_same_suit += 1
                straight_flush_memory = [last_seen.suit, sequential_in_a_row_same_suit, card.value-1]
            else:
                sequential_in_a_row_same_suit = 1
            #dealing with straights
            if sequential_in_a_row == 5:
                if sequential_in_a_row_same_suit == 5: #NOTE, SOME STRAIGHT FLUSHES WILL BE IGNORED IF THERE ARE TWO SEQUENTIAL CARDS OF THE SAME TYPE IF THE ONE OF NON-MATCHING SUIT IS SCANNED FIRST
                    return (8, card.value)
                elif straight == None:
                    straight = (4, card.value)
        elif card.value == last_seen.value:
            same_in_a_row += 1
        else:
            sequential_in_a_row = 1
            sequential_in_a_row_same_suit = 1
            #processing pairs
            if same_in_a_row in matches.keys():
                matches[same_in_a_row][0] += 1
                if matches[same_in_a_row][1] == None:
                    matches[same_in_a_row][1] = last_seen.value
            same_in_a_row = 1
        if straight_flush_memory[0] == card.suit and straight_flush_memory[2] == card.value:
            sequential_in_a_row_same_suit = straight_flush_memory[1]+1
        if sequential_in_a_row_same_suit == 5: #NOTE, SOME STRAIGHT FLUSHES WILL BE IGNORED IF THERE ARE TWO SEQUENTIAL CARDS OF THE SAME TYPE IF THE ONE OF NON-MATCHING SUIT IS SCANNED FIRST
            return (8, card.value)
        last_seen = card
    #going through all possible values to see what to return
    if matches[4][0] > 0:
        return (7, matches[4][1])
    if matches[3][0] >= 1 and matches[2][0] >= 1:
        return (6, matches[3][1]) 
    for suit, vals in suits.items():
        if vals[0] >= 5:
            return (5, vals[1])
    if straight:
        return straight
    if matches[3][0] >= 1:
        return (3, matches[3][1])
    if matches[2][0] >= 2:
        return (2,matches[2][1])
    if matches[2][0] >= 1:
        return (1, matches[2][1])
    return (0, cards[0].value)

def victor(field, hand, otherhand):
    """
    Returns d for draw, w if hand beats otherhand, and l if otherhand wins.
    """
    handval = find_best_hand(hand,field)
    otherhandval = find_best_hand(otherhand, field)
    if handval[0] == otherhandval[0]:
        if handval[1] == otherhandval[1]:
            return "D"
        if handval[1] > otherhandval[1]:
            return "W"
        return "L"
    if handval[0] > otherhandval[0]:
        return "W"
    return "L"