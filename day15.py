import re


def xmas_hash(s):
    cur_val = 0
    for c in s:
        ascii_val = ord(c)
        # print("char is {}, ord is {}".format(c, ascii_val))
        cur_val += ascii_val
        cur_val *= 17
        cur_val %= 256

    return cur_val

class Box(object):
    def __init__(self, id):
        self.id = id
        self.lenses = []

    def remove(self, target_label):
        for idx, (l, focal) in enumerate(self.lenses):
            if l == target_label:
                self.lenses.pop(idx)
                break 

    def insert(self, new_label, new_focal):
        for idx, (l, focal) in enumerate(self.lenses):
            if l == new_label:
                self.lenses[idx] = (new_label, new_focal)
                return
        self.lenses.append((new_label, new_focal))

    def __str__(self):
        buf = []
        for l, f in self.lenses:
            s = '[{} {}]'.format(l, f)
            buf.append(s)
        return ' '.join(buf)
    
    def focus_power(self):
        acc = 0
        for idx, (_, focal) in enumerate(self.lenses):
            acc += (1 + self.id) * (idx + 1) * focal
        return acc


class Laser(object):
    def __init__(self, i_strings):
        i_re = re.compile(r'(?P<label>[a-z]+)(?P<op>[=-])(?P<val>\d+)?')
        boxes = [Box(int(i)) for i in range(0, 256)]
        for i in i_strings:
            res = i_re.match(i)
            label, op, val = res.group('label'), res.group('op'), res.group('val')
            print(xmas_hash(label))
            dst_box = boxes[xmas_hash(label)]
            if op == '-':
                dst_box.remove(label)
            else:
                dst_box.insert(label, int(val))
        self.boxes = boxes

    def __str__(self):
        buf = ''
        for b_id, b in enumerate(self.boxes):
            if len(b.lenses):
                s = "Box {}: {}\n".format(b_id, str(b))
                buf += s
        return buf
    
    def total_power(self):
        acc = 0
        for b in self.boxes:
            acc += b.focus_power()
        return acc

if __name__ == "__main__":
    f = open('input_day15.txt', 'r')
    line = f.read()
    steps = line.split(',')
    l = Laser(steps)
    print(l)
    print(l.total_power())
