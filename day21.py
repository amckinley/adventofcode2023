import os
import itertools
from enum import Enum

class Tile(Enum):
    START = 'S'
    ROCK = '#'
    SPACE = '.'

class Garden(object):
    def __init__(self, lines):
        tiles = []
        for r_idx, l in enumerate(lines):
            l = l.strip()
            row = []
            for c_idx, c in enumerate(l):
                t = Tile(c)
                row.append(t)
                if t == Tile.START:
                    self.start_addr = (r_idx, c_idx)
            tiles.append(row)
        self.tiles = tiles
        print("rows = {}, cols = {}".format(len(tiles), len(tiles[0])))
    
    def __str__(self):
        return self._internal_str(set())
    
    def highlight(self, addrs):
        return self._internal_str(addrs)
    
    def _internal_str(self, addrs):
        buf = ''
        for r_idx, row in enumerate(self.tiles):
            row_buf = ''
            for c_idx, c in enumerate(row):
                if (r_idx, c_idx) in addrs:
                    row_buf += 'O'
                else:
                    row_buf += c.value
            buf += row_buf + '\n'

        return buf[:-1]

    
    '''
    Keep a set of all our current locations. For every step, pop them all, create new set
    '''
    def start_walk(self, steps):
        target_steps = steps
        cur = set()
        cur.add(self.start_addr)

        while steps:
            next = set()
            for addr in cur:
                next.update(self.valid_steps_from(addr))
            cur = next
            steps -= 1
            # print("after {} steps".format(target_steps - steps))
            print(self.highlight(cur))
            os.system("cls")

        print("total reachable = {}".format(len(cur)))

    '''
    Try to compute the dimensions of our diamond shape
    '''
    def find_shape_area(self):
        midpoint_row = 65 - 1
        midpoint_col = 65 - 1
        num_cols = len(self.tiles[0])
        num_rows = len(self.tiles)
        #          left edge         right edge                top edge            # bottom edge
        points = [(midpoint_row, 0), (midpoint_row, num_cols-1), (0, midpoint_col), (num_rows-1, midpoint_col)]

        sum = 0
        for (a_r, a_c), (b_r, b_c) in itertools.pairwise(points):
            sum += (a_c + b_c) * (a_r - b_r)
        
        sum *= 0.5
        sum = abs(sum)
        print("area is {}".format(sum))
        # print([self.is_valid(p) for p in points])


    '''
    Returns the (up to 4) valid addresses from this tile
    '''
    def valid_steps_from(self, addr):
        r, c = addr
        up = r-1, c
        down = r+1, c
        left = r, c-1
        right = r, c+1
        options = [up, down, left, right]
        return [o for o in options if self.is_valid(o)]

    '''
    True if the address is in bounds and not a rock
    '''
    def is_valid(self, addr):
        r, c = addr
        return r >= 0 and r < len(self.tiles) and \
            c >= 0 and c < len(self.tiles[0]) and \
            self.tiles[r][c] != Tile.ROCK

if __name__ == "__main__":
    f = open('input_day21.txt', 'r')
    g = Garden(f.readlines())
    g.find_shape_area()
    # print(str(g))
    # g.start_walk(64)