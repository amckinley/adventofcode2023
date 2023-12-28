def solve(lines):
    acc = 0
    for l in lines:
        first = -1
        last = -1
        for c in l:
            if c.isdigit():
                if first == -1:
                    first = int(c)
                last = int(c)

        acc += first * 10 + last
    return acc

def solve_spelled(lines):
    digits = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9 
    }
    
    acc = 0
    for l in lines:
        first = -1
        last = -1
        for idx, c in enumerate(l):
            tail = l[idx:]
            # print(tail)
            
            # easy check first
            if c.isdigit():
                if first == -1:
                    first = int(c)
                last = int(c)

            # check all the words
            else:
                for word, val in digits.items():
                    if tail.startswith(word):
                        if first == -1:
                            first = int(val)
                        last = int(val)

        print("{} {}{}".format(l, first, last))
        acc += first * 10 + last
    return acc





if __name__ == "__main__":
#     ex = '''1abc2
# pqr3stu8vwx
# a1b2c3d4e5f
# treb7uchet'''
#     lines = ex.splitlines()

#     print(solve(lines))
    file1 = open('data.txt', 'r')
    lines = file1.readlines()

    ex = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen'''
    print(solve_spelled(lines))