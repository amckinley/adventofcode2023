import itertools

class Node(object):
    def __init__(self, id, l, r):
        self.id = id
        self.l = l
        self.r = r

    def __str__(self):
        return "{} -> ['{}', '{}']".format(self.id, self.l, self.r)
    
if __name__ == "__main__":
    file1 = open('input_day8.txt', 'r')
    
    moves = file1.readline().strip()
    file1.readline()
    node_lines = file1.readlines()


    node_map = {}
    for l in node_lines:
        id, l_r = l.split("=")
        l, r = l_r.split(",")
        id, l, r = id.strip(), l.strip(), r.strip()
        l = l[1:]
        r = r[:-1]
        n = Node(id, l, r)
        node_map[id] = n

    cur_id = 'AAA'
    move_cnt = 0
    for dir in itertools.cycle(moves):
        if cur_id == 'ZZZ':
            break
        cur_node = node_map[cur_id]
        next_id = getattr(cur_node, dir.lower())
        # print('moving from node {} to choice {}, id {}'.format(cur_node, dir, next_id))
        cur_id = next_id
        move_cnt += 1

    print(move_cnt)
