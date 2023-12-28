from collections import defaultdict
import math

class Schematic(object):
    def __init__(self, lines):
        self.raw = lines
        self.rows = len(lines)
        self.cols = len(lines[0])
        self.numbers = self.find_numbers()
        self.symbols = self.find_symbols()
        self.gears = self.find_gears()
        self.live_parts = self.find_live_parts()
        # print(self.live_parts)
        # print(sum(self.live_parts))


        # print(sorted(self.find_neighbors(self.numbers[0])))

    def valid(self, row, col):
        return row >= 0 and row <= self.rows and col >= 0 and col <= self.cols

    # go through all the numbers, looking for ones that are correctly adjacent to a symbol
    def find_live_parts(self):
        live = []
        adjacency_map = defaultdict(list)
        for n in self.numbers:
            neighbors = self.find_neighbors(n)
            for row, col in neighbors:
                if self.is_symbol(row, col):
                    # map from symbols to the part numbers that are adjacent to them
                    adjacency_map[(row, col)].append(n)
                    live.append(n['id'])
                    break

        acc = 0
        for coords, parts in adjacency_map.items():
            row, col = coords
            if len(parts) == 2:
                ratio = math.prod([ p['id'] for p in parts ])
                acc += ratio
                print("{} {}: {}".format(row, col, ratio))

        print(acc)
        return live
    
    def find_numbers(self):
        part_numbers = []
        for row, l in enumerate(self.raw):
            buf = ''
            start = end = -1
            in_digit = False
            for c_idx, c in enumerate(l):
                if in_digit:
                    # continuing existing part
                    if c.isdigit():
                        buf += c
                    
                    # prev char was end of part
                    else:
                        end = c_idx - 1
                        in_digit = False
                        part = {'id': int(buf), 'row': row, 'col': start, 'len': len(buf)}
                        part_numbers.append(part)
                        buf = ''
                
                else:
                    # starting new part
                    if c.isdigit():
                        in_digit = True
                        buf += c
                        start = c_idx
        
        return part_numbers

    def find_symbols(self):
        symbols = []
        for row, l in enumerate(self.raw):
            l = l.strip()
            for col, c in enumerate(l):
                if c == '.' or c.isdigit():
                    continue
                else:
                    symbols.append((row, col))

        return symbols
    
    def find_gears(self):
        gears = set()
        for row, col in self.symbols:
            val = self.raw[row][col]
            if val == '*':
                gears.add((row, col))
        
        return gears


    def is_symbol(self, row, col):
        return (row, col) in self.symbols

    def find_neighbors(self, part):
        row = part['row']
        col = part['col']
        length = part['len']
        neighbors = set()
        
        # test left
        neighbors.add((row, col-1))

        # test right
        neighbors.add((row, col+length))

        # test above
        for i in range(length):
            neighbors.add((row-1, col+i))

        # test below
        for i in range(length):
            neighbors.add((row+1, col+i))

        # bottom left
        neighbors.add((row+1, col-1))

        # bottom right
        neighbors.add((row+1, col+length))

        # top left
        neighbors.add((row-1, col-1))

        # top right
        neighbors.add((row-1, col+length))

        # print("before check {}".format(neighbors))
        # test all points
        return [ (r,c) for r, c in neighbors if self.valid(r, c) ]

if __name__ == "__main__":
    file1 = open('day3.txt', 'r')
    # file1 = open('input_day3_ex.txt', 'r')
    lines = file1.readlines()
    schem = Schematic(lines)
    # print(schem.schem_numbers())
    schem.find_symbols()