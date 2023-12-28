from collections import defaultdict
from enum import Enum

class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    

class HandRank(OrderedEnum):
    FIVE_OAK = 7
    FOUR_OAK = 6
    FULL_HOUSE = 5
    THREE_OAK = 4
    TWO_PAIR = 3
    PAIR = 2
    HIGH_CARD = 1

class CardRank(OrderedEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    # def __cmp__(self, other):
    #     pass

class Hand(object):
    RANK_MAP = {
        'A': CardRank.ACE,
        'K': CardRank.KING,
        'Q': CardRank.QUEEN,
        'J': CardRank.JACK,
        'T': CardRank.TEN,
        '9': CardRank.NINE,
        '8': CardRank.EIGHT,
        '7': CardRank.SEVEN,
        '6': CardRank.SIX,
        '5': CardRank.FIVE,
        '4': CardRank.FOUR,
        '3': CardRank.THREE,
        '2': CardRank.TWO
    }

    def __init__(self, hand_s):
        hand_s, bid = hand_s.split(" ")
        self.bid = int(bid)
        self.raw = hand_s
        self.rank_map = self.to_rank_map()
        r = None
        m_r = None
        if self.is_five_oak():
            r = HandRank.FIVE_OAK
            m_r = self.five_oak_minor()
        elif self.is_four_oak():
            r = HandRank.FOUR_OAK
            m_r = self.four_oak_minor()
        elif self.is_full_house():
            r = HandRank.FULL_HOUSE
            m_r = self.full_house_minor()
        elif self.is_three_oak():
            r = HandRank.THREE_OAK
            m_r = self.three_oak_minor()
        elif self.is_two_pair():
            r = HandRank.TWO_PAIR
            m_r = self.two_pair_minor()
        elif self.is_pair():
            r = HandRank.PAIR
            m_r = self.pair_minor()
        else:
            r = HandRank.HIGH_CARD
            m_r = self.high_card_minor()
        self.major_rank = r
        self.minor_rank = m_r

    def __str__(self):
        inv_hand_map = {v: k for k, v in Hand.RANK_MAP.items()}
        
        # build rank_map but with CardRank objects
        rank_map = defaultdict(int)
        for c in self.raw:
            rank_map[Hand.RANK_MAP[c]] += 1

        # sort the list of tuples
        sorted_ranks = sorted(rank_map.items(), reverse=True)
        
        # build the n>1 part of the string
        hand_s = ''
        kickers = []
        for r, cnt in sorted_ranks:
            if cnt == 1:
                kickers.append(r)
                continue
            s = inv_hand_map[r] * cnt
            hand_s += s
        
        # sort the kickers
        kickers = sorted(kickers, reverse=True)

        # kickers back to strings
        kickers_s = ''.join([inv_hand_map[r] for r in kickers])

        hand_s += kickers_s
        return hand_s

    def is_five_oak(self):
        return 5 in self.rank_map.values()
    
    # returns rank of foak (done)
    def five_oak_minor(self):
        for r, cnt in self.rank_map.items():
            if cnt == 5:
                return self.RANK_MAP[r]
        raise Exception("wtf no minor")

    def is_four_oak(self):
        return 4 in self.rank_map.values()
    
    # returns (foak_rank, kicker) (done)
    def four_oak_minor(self):
        foak_rank = None
        kicker_rank = None
        for r, cnt in self.rank_map.items():
            if cnt == 4:
                foak_rank = self.RANK_MAP[r]
            elif cnt == 1:
                kicker_rank = self.RANK_MAP[r]
            else:
                raise Exception("wtf no minor {} {}".format(self, cnt))
        
        if not foak_rank or not kicker_rank:
            raise Exception("wtf no minor")
        
        return (foak_rank, kicker_rank)

    def is_full_house(self):
        return 3 in self.rank_map.values() and 2 in self.rank_map.values()

    # returns (set_rank, pair_rank) (done)
    def full_house_minor(self):
        trips = None
        pair = None
        for r, cnt in self.rank_map.items():
            if cnt == 3:
                trips = self.RANK_MAP[r]
            elif cnt == 2:
                pair = self.RANK_MAP[r]
        if not trips or not pair:
            raise Exception("wtf no minor")
        
        return (trips, pair)

    def is_three_oak(self):
        return 3 in self.rank_map.values()
    
    # returns (set_rank, kick1_rank, kick2_rank) (done)
    def three_oak_minor(self):
        set_rank = None
        kicks = []
        for r, cnt in self.rank_map.items():
            if cnt == 3:
                set_rank = self.RANK_MAP[r]
            elif cnt == 1:
                kicks.append(self.RANK_MAP[r])
        
        if not set_rank or not len(kicks) == 2:
            raise Exception("wtf no minor")
        
        return set_rank, sorted(kicks, reverse=True)
        
    def is_two_pair(self):
        pair_cnt = 0
        for r, cnt in self.rank_map.items():
            if cnt == 2:
                pair_cnt += 1

        return pair_cnt == 2
    
    # returns (top_pair_rank, bottom_pair_rank, kicker_rank) (done)
    def two_pair_minor(self):
        pairs = []
        kicker = None
        for r, cnt in self.rank_map.items():
            if cnt == 2:
                pairs.append(self.RANK_MAP[r])
            elif cnt == 1:
                kicker = self.RANK_MAP[r]
            else:
                raise Exception("wtf no minor")
            
        pairs = sorted(pairs, reverse=True)
        return (pairs, kicker)
        
    def is_pair(self):
        return 2 in self.rank_map.values()
    
    # returns (pair_rank, kick1_rank, kick2_rank, kick3_rank)
    def pair_minor(self):
        pair = None
        kicks = []
        for r, cnt in self.rank_map.items():
            if cnt == 2:
                pair = self.RANK_MAP[r]
            elif cnt == 1:
                kicks.append(self.RANK_MAP[r])
            else:
                raise Exception("wtf")
        
        if not pair or len(kicks) != 3:
            raise Exception("wtf")
        
        kicks = sorted(kicks, reverse=True)
        return pair, kicks

    # returns (kick1_rank, kick2_rank, kick3_rank, kick4_rank, kick5_rank)
    def high_card_minor(self):
        ranks = sorted([self.RANK_MAP[c] for c in self.raw], reverse=True)
        return ranks

    def to_rank_map(self):
        rank_map = defaultdict(int)
        for c in self.raw:
            rank_map[c] += 1

        return rank_map
        
    def __lt__(self, other):
        if self.major_rank != other.major_rank:
            return self.major_rank < other.major_rank
        
        self_minor = [self.RANK_MAP[c] for c in self.raw]
        other_minor = [self.RANK_MAP[c] for c in other.raw]
        
        for s, o in zip(self_minor, other_minor):
            if s != o:
                return s < o
        # return (self.major_rank, self.minor_rank) < (other.major_rank, other.minor_rank)



if __name__ == "__main__":

#     hand_lines = '''AAAAA
# AA8AA
# 23332
# TTT98
# 23432
# A23A4
# 23456
# '''
    hand_lines = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''.splitlines()
# failed
# 250688365
    file1 = open('input_day7.txt', 'r')
    hand_lines = file1.readlines()

    hands = []
    for l in hand_lines:
        h = Hand(l)
        hands.append(h)
        # print(h)
        # print("{} {}".format(h.major_rank, h.minor_rank))

    sum = 0
    hands = sorted(hands)
    for idx, h in enumerate(hands):
        print("{} {} {} {}".format(idx, h.major_rank, h, h.raw))
        sum += h.bid * (idx+1)

    print(sum)