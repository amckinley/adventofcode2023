class Almanac(object):
    def __init__(self, lines):
        for l in lines:
            if l.startswith("seeds:"):
                _, seeds = l.split("seeds:")
                self.seeds = [int(s) for s in seeds.split(" ") if s]

if __name__ == "__main__":
    file1 = open('input_day5_ex.txt', 'r')
    lines = file1.readlines()

    a = Almanac(lines)