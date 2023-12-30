from enum import Enum, auto
from collections import defaultdict, deque
from colorama import just_fix_windows_console, Fore, Back, Style
import sys
import itertools

class Tile(Enum):
    ROUND = 'O'
    SQUARE = '#'
    SPACE = '.'

class Platform(object):
    def __init__(self, lines):
        tiles = []
        for row, l in enumerate(lines):
            l = l.strip()
            new_row = [Tile(c) for c in l]
            tiles.append(new_row)
        self.tiles = tiles

    # def __eq__(self, other):
    #     return self.tiles == other.tiles
    
    # def __hash__(self, other):
    #     return hash(str(self)) == hash(str(other))

    def __str__(self):
        return self.__internal_str__(set())
    
    def str_colorized(self, colorized):
        return self.__internal_str__(colorized)
    
    def __internal_str__(self, colorize):
        buf = ''
        for r_id, row in enumerate(self.tiles):
            row_buf = ''
            for c_id, c in enumerate(row):
                if (r_id, c_id) in colorize:
                    row_buf += Fore.RED + c.value + Style.RESET_ALL
                else:
                    row_buf += c.value
            buf += row_buf + '\n'

        return buf[:-1]
    
    def iter_cols(self):
        for col_id in range(len(self.tiles[0])):
            buf = []
            for row_id, row in enumerate(self.tiles):
                buf.append((row[col_id], (row_id, col_id)))
            yield buf

    def iter_rows(self):
        for row_id, row in enumerate(self.tiles):
            yield [(tile, (row_id, col_id)) for col_id, tile in enumerate(row)]

    def roll_north(self):
        for col in self.iter_cols():
            self.roll_slice(col)

    def roll_south(self):
        for col in self.iter_cols():
            self.roll_slice(reversed(col))

    def roll_east(self):
        for row in self.iter_rows():
            self.roll_slice(reversed(row))

    def roll_west(self):
        for row in self.iter_rows():
            self.roll_slice(row)

    def spin(self):
        self.roll_north()
        self.roll_west()
        self.roll_south()
        self.roll_east()

    '''
    this is how we roll the platform in arbitrary directions, one row or col at a time.
    it takes a list where each item is a (tile, (row_id, col_id)).
    its the caller's job to put the list in order so we can traverse left to right,
    where the left side is "down"
    '''
    def roll_slice(self, slice):
        open_spots = deque()
        for tile, addr in slice:
            match tile:
                case Tile.SQUARE:
                    open_spots.clear()
                case Tile.SPACE:
                    open_spots.append(addr)
                case Tile.ROUND:
                    if len(open_spots):
                        dst_addr = open_spots.popleft()
                        self.swap(addr, dst_addr)
                        # we just opened up this tile, and by definition it must go at the end of the list
                        open_spots.append(addr)

    def calculate_load(self):
        acc = 0
        factor = len(self.tiles)
        for r_id, row in enumerate(self.tiles):
            rock_cnt = row.count(Tile.ROUND)
            acc += rock_cnt * factor
            factor -= 1

        return acc

    def swap(self, a_addr, b_addr):
        a_row, a_col = a_addr
        b_row, b_col = b_addr
        temp = self.tiles[a_row][a_col]
        self.tiles[a_row][a_col] = self.tiles[b_row][b_col]
        self.tiles[b_row][b_col] = temp

    # takes the correct platform and prints out a colorized delta
    def print_delta_from_answer(self, other):
        wrong = set()
        for r_id, row in enumerate(self.tiles):
            for c_id, t in enumerate(row):
                if self.tiles[r_id][c_id] != other.tiles[r_id][c_id]:
                    wrong.add((r_id, c_id))

        print(self.str_colorized(wrong))

if __name__ == "__main__":
    # get colorama working
    just_fix_windows_console()

    f = open('input_day14.txt', 'r')
    p = Platform(f.readlines())

    spins_to_cnt_map = {}
    cnt_to_spins_map = {}
    offset = -1
    period = -1
    for cnt in itertools.count(start=1):
        p.spin()
        cur_val = str(p)
        if cur_val in spins_to_cnt_map:
            offset = spins_to_cnt_map[cur_val]
            period = cnt - offset
            break
        spins_to_cnt_map[cur_val] = cnt
        cnt_to_spins_map[cnt] = cur_val

    target = 1000000000 - offset
    target = target % period
    target_platform_str = cnt_to_spins_map[offset + target]

    p_target = Platform(target_platform_str.split("\n"))
    print(p_target.calculate_load())