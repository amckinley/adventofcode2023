import itertools
import math
import sys
import numpy as np

class Image(object):
    def __init__(self, raw):
        self.raw = raw
        expansion_factor = 2

        # find lines to expand
        rows_needed = []
        for r_idx, r in enumerate(raw.splitlines()):
            if '#' in set(r):
                continue
            else:
                rows_needed.append(r_idx)

        fixed_rows = []
        for r_idx, r in enumerate(raw.splitlines()):
            fixed_rows.append(r)
            if r_idx in rows_needed:
                for i in range(expansion_factor - 1):
                    fixed_rows.append(r)

        print("rows expanded")

        # find cols to expand
        cols_needed = []
        for c_idx, c in enumerate(self.get_raw_cols(fixed_rows)):
            if '#' in set(c):
                continue
            else:
                cols_needed.append(c_idx)
        
        # calculate the final size
        num_regular_rows = len(raw.splitlines())
        num_expanded_rows = len(rows_needed)
        total_rows = num_regular_rows + (num_expanded_rows * (expansion_factor - 1))
        print("total {}, len fixed {}".format(total_rows, len(fixed_rows)))
        assert total_rows == len(fixed_rows)
        total_rows = len(fixed_rows)
    
        num_regular_cols = len(fixed_rows[0])
        num_expanded_cols = len(cols_needed)
        total_cols = num_regular_cols + (num_expanded_cols * (expansion_factor - 1))
        
        # output the fully corrected image
        image = np.empty((total_rows, total_cols))
        for r_idx, row in enumerate(fixed_rows):
           for c_idx, c in enumerate(row):

                if c_idx in cols_needed:
                    for i in range(expansion_factor):
                        image[r_idx][c_idx + i] = 1
                else:
                    image[r_idx][c_idx] = 0

        print(image)

        # # first make all the inner arrays
        # for i in range(len(fixed_rows)):
        #     image.append([])

        # # then iterate over the row data, writing double vals as needed
        # row_count = float(len(fixed_rows))
        # for r_idx, row in enumerate(fixed_rows):
                    
        #     for c_idx, c in enumerate(row):
        #         image[r_idx].append(c)
        #         if c_idx in cols_needed:
        #             for i in range(expansion_factor - 1):
        #                 image[r_idx].append(c)

        print("cols expanded")
        print("len image {}, total_cols {}".format(len(image[0]), total_cols))
        assert len(image[0]) == total_cols

        self.image = image
        self.num_rows = len(image)
        self.num_cols = len(image[0])
        self.asssign_ids()
        print("galaxies {}".format(self.galaxies))

    # give an ID to every galaxy
    def asssign_ids(self):
        idx = 1
        galaxies = {}
        for (r_idx, c_idx), c in self.get_all_cells():
            if c == 1:
                galaxies[idx] = (r_idx, c_idx)
                idx += 1
        self.galaxies = galaxies

    def find_all_path_lens(self):
        distances = {}
        for g1_idx, g2_idx in itertools.combinations(self.galaxies.keys(), 2):
            g1 = self.galaxies[g1_idx]
            g2 = self.galaxies[g2_idx]
            # print("working on {} {}".format(g1_idx, g2_idx))
            dis = self.manhattan_distance(g1, g2)
            distances[(g1, g2)] = dis
        
        return distances
        

    # def find_path_len(self, g1, g2):
    #     s_row, s_col = self.galaxies[g1]
    #     f_row, f_col = self.galaxies[g2]
    #     visited = set()
    #     to_visit = []
    #     to_visit.append((s_row, s_col, 0))

    #     while True:
    #         c_row, c_col, distance = to_visit.pop()
    #         visited.add((c_row, c_col))
    #         if c_row == f_row and c_col == f_col:
    #             return distance

    #         for r, c in self.get_neighbors(c_row, c_col):
    #             if not (r, c) in visited:
    #                 to_visit.append((r, c, distance+1))


    def get_neighbors(self, row, col):
        neighbor_candidates = [
            (row-1, col),
            (row+1, col),
            (row, col-1),
            (row, col+1)]
        
        for r, c in neighbor_candidates:
            if self.is_valid_cell(r, c):
                yield (r, c)
        

    def is_valid_cell(self, row, col):
        return row >= 0 and row < self.num_cols and col >= 0 and col < self.num_cols

    def num_galaxies(self):
        return len(self.galaxies.keys())
    
    def get_all_cells(self):
        for r_idx, row in enumerate(self.get_rows()):
            for c_idx, c in enumerate(row):
                yield (r_idx, c_idx), c

    def get_rows(self):
        return self.image
    
    def get_raw_rows(self):
        return self.raw.splitlines()
    
    def manhattan_distance(self, g1, g2):
        dis = 0
        for i in range(len(g1)):
            dis += abs(g1[i] - g2[i])
        return dis

    def get_raw_cols(self, rows=None):
        if not rows:
            rows = self.raw.splitlines()
        for c_idx in range(len(rows[0])):
            col = []
            for r in self.get_raw_rows():
                col.append(r[c_idx])
            yield col
            
if __name__ == "__main__":
    example = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''
    img = Image(example)
    # img = Image(open('input_day11.txt', 'r').read())
    distances = img.find_all_path_lens()
    d_sum = 0
    for (g1, g2), d in distances.items():
        # print("computed ({}->{}) = {}".format(g1, g2, d))
        d_sum += d
    print(d_sum)

    # g1 = img.galaxies[5]
    # g2 = img.galaxies[9]
    # print("g1 {}, g2 {}, distance {}".format(g1, g2, img.find_path_len(5, 9)))
    # print("math {}, man {}".format(math.dist(g1, g2), img.manhattan_distance(g1, g2)))
    # print("1-7 {}, 3-6 {}, 8-9 {}".format(
    #     img.manhattan_distance(img.galaxies[1], img.galaxies[7]),
    #     img.manhattan_distance(img.galaxies[3], img.galaxies[6]),
    #     img.manhattan_distance(img.galaxies[8], img.galaxies[9])))

