from collections import defaultdict

class Scratcher(object):
    def __init__(self, line):
        winners, mine = line.split(" | ")
        id, winners = winners.split(": ")
        id = id[4:]
        winners = set([int(c) for c in winners.split(" ") if len(c) > 0])
        mine = set([int(c) for c in mine.split(" ") if len(c) > 0])

        hits = winners.intersection(mine)
        value = len(hits)
        # if hits:
        #     value = 2 ** (len(hits) -1 )
        # else:
        #     value = 0

        self.id = int(id)
        self.winners = winners
        self.mine = mine
        self.value = value
        # print("id: {}, value:{}, winners: {}, mine: {}".format(id, value, winners, mine))
    
    def get_output_card_ids(self):
        return [p + 1 for p in range(self.id, self.id + self.value)]

if __name__ == "__main__":
    # file1 = open('day3.txt', 'r')
    file1 = open('input_day4.txt', 'r')
    lines = file1.readlines()

    scratchers = {}
    for l in lines:
        s = Scratcher(l)
        scratchers[s.id] = s
        # print("{} {}".format(s.id, s.get_output_card_ids()))
    
    stack = []
    counts = {}
    for s in scratchers.values():
        stack.append(s)
        counts[s.id] = 1

    while stack:
        s = stack.pop()
        for id in s.get_output_card_ids():
            new_s = scratchers[id]
            stack.append(new_s)
            counts[id] += 1
    
    total = 0
    for id, cnt in sorted(counts.items()):
        print("{} {}".format(id, cnt))
        total += cnt
    
    print("total: {}".format(total))