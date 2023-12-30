from enum import Enum, auto
from collections import defaultdict, deque
from colorama import just_fix_windows_console, Fore, Back, Style
import sys

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
        self.colorize = set()

    def __str__(self):
        buf = ''
        for r_id, row in enumerate(self.tiles):
            row_buf = ''
            for c_id, c in enumerate(row):
                if (r_id, c_id) in self.colorize:
                    row_buf += Fore.RED + c.value + Style.RESET_ALL
                else:
                    row_buf += c.value
            buf += row_buf + '\n'

        return buf[:-1]
    
    # this is a stupid hack. takes set((row, col)) addresses to highlight
    # on the next invocation of str()
    def mark_for_colorize(self, colorize):
        self.colorize = colorize
    
    def iter_cols(self):
        for col_id in range(len(self.tiles[0])):
            buf = []
            for row in self.tiles:
                buf.append(row[col_id])
            yield buf

    def roll_north(self):
        for c_id, col in enumerate(self.iter_cols()):
            # print("working on {}".format(c_id))
            # track all the available open spots. when we find a square rock, pop everything out
            open_spots = deque()

            # now loop across the rows in the col
            for r_id, cell in enumerate(col):
                match cell:
                    case Tile.SQUARE:
                        open_spots.clear()
                    case Tile.SPACE:
                        open_spots.append(r_id)
                    case Tile.ROUND:
                        if len(open_spots):
                            r_dst = open_spots.popleft()
                            self.swap_within_col(c_id, r_id, r_dst)
                            # we just opened up this tile, and by definition it must go at the end of the list
                            open_spots.append(r_id)
                            
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


    def swap_within_col(self, col, a_row, b_row):
        a_addr = a_row, col
        b_addr = b_row, col
        self.swap(a_addr, b_addr)

    # takes the correct platform and prints out a colorized delta
    def print_delta_from_answer(self, other):
        wrong = set()
        for r_id, row in enumerate(self.tiles):
            for c_id, t in enumerate(row):
                if self.tiles[r_id][c_id] != other.tiles[r_id][c_id]:
                    wrong.add((r_id, c_id))

        self.mark_for_colorize(wrong)
        print(self)



if __name__ == "__main__":
    # get colorama working
    just_fix_windows_console()

    f = open('input_day14.txt', 'r')
    p = Platform(f.readlines())
    # print(p)
    # print()
    p.roll_north()
    # cols = list(p.iter_cols())
    # print(''.join([c.value for c in cols[0]]))

    # f_ans = open('input_day14_ex_ans.txt', 'r')
    # ans = Platform(f_ans.readlines())
    # p.print_delta_from_answer(ans)
    print(p.calculate_load())