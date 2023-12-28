import sys
import itertools

class Trench(object):
    def __init__(self, lines):
        # first we build a list of every corner defining the polygon, relative
        # to an origin of (0,0) on the cartesian plane
        trench_len = 0
        x, y = 0, 0
        points = [(x, y)]
        dir_map = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
        for l in lines:
            l = l.strip()
            _, _, color = l.split(' ')
            color = color.strip('()')
            
            # split into first 5/last 1
            cnt, dir = color[1:-1], color[-1:]
            
            # convert from hex, int to direction
            cnt, dir = int(cnt, 16), dir_map[dir]

            trench_len += cnt
            match dir:
                case 'U':
                    new_x = x
                    new_y = y + cnt
                case 'D':
                    new_x = x
                    new_y = y - cnt
                case 'L':
                    new_x = x - cnt
                    new_y = y
                case 'R':
                    new_x = x + cnt
                    new_y = y
            points.append((new_x, new_y))
            x = new_x
            y = new_y
        
        # check for return to origin
        if new_x != 0 or new_y != 0:
            print("what")
            sys.exit(-1)

        self.points = points
        self.trench_len = trench_len

    def find_area(self):
        # same technique from day2: Shoelace Formula to find the interior area.
        sum = 0
        for (x1, y1), (x2, y2) in itertools.pairwise(self.points):
            sum += (y1 + y2) * (x1 - x2)

        sum *= 0.5
        sum = abs(sum)

        # now use Pick's Theorem to calculate interior points
        interior = sum - (self.trench_len/2) + 1

        # add interior points to boundary points to compute total area
        print("area is {}, interior {}, total {}".format(
            sum, interior, interior + self.trench_len))


if __name__ == "__main__":
    f = open('input_day18.txt', 'r')
    t = Trench(f.readlines())
    t.find_area()