import re
from collections import defaultdict
import itertools
from math import prod

class Rule(object):
    def __init__(self, prop, cmp, val, dst):
        self.prop = prop
        self.cmp = cmp
        self.val = int(val)
        self.dst = dst

    def __str__(self):
        return "{}{}{}:{}".format(self.prop, self.cmp, self.val, self.dst)
    
    def get_accepting_set(self):
        if self.cmp == '>':
            return (self.prop, set(range(self.val, 4000)))
        else:
            return (self.prop, set(range(0, self.val)))
    
class DefaultRule(Rule):
    def __init__(self, dst):
        self.dst = dst
        self.cmp = None
    
    def __str__(self):
        return self.dst
    
class Workflow(object):
    def __init__(self, line):
        self.line = line
        expr = re.compile(r"(?P<name>[a-z]+)\{(?P<rules>\S+)\}")
        res = expr.match(line)
        # print("({}) ({})".format(line, res))
        # print("({}) ({})".format(res.groups('name'), res.group('rules')))
        self.name = res.group('name')
        
        # split the rules into the conditionals and the default
        rule_s = res.group('rules')
        rule_parts = rule_s.split(',')
        rule_default = DefaultRule(rule_parts[-1])
        rule_s = ' '.join(rule_parts[:-1])
        expr = re.compile(
            r'(?P<prop>[xmas])(?P<cmp>[<>])(?P<val>\d+)\:(?P<dest>[a-zAR]+)+')
        matches = expr.findall(rule_s)
        rules = []
        for m in matches:
            r = Rule(*m)
            rules.append(r)
        rules.append(rule_default)
        self.rules = rules

    def get_children_names(self):
        return [r.dst for r in self.rules]

    def __str__(self):
        return "WID-{}".format(self.name)
    
class TerminalWorkflow(Workflow):
    def __init__(self, name):
        self.name = name
        self.rules = []


class Graph(object):
    def __init__(self, lines):
        workflow_lines = []
        for l in lines:
            if l == '\n':
                break

            workflow_lines.append(l.strip())

        # adjacency list, looks like {
        #    'in': [Obj, Obj],
        #    'bar': [Obj]
        # }
        # first we build the map from names => Workflows, then we go back
        # and build the adjacency list
        workflows = {}
        workflows['A'] = TerminalWorkflow('A')
        workflows['R'] = TerminalWorkflow('R')
        for l in workflow_lines:
            w = Workflow(l)
            workflows[w.name] = w
        self.workflows = workflows

        adjacency_list = defaultdict(list)
        for w_name, w in workflows.items():
            c_names = w.get_children_names()
            for c in c_names:
                adjacency_list[w_name].append(workflows[c])
                 
        self.adjacency_list = adjacency_list
        # for w_name, children in adjacency_list.items():
        #     print("{}: [{}]".format(w_name, ",".join([c.name for c in children])))

        # this is kind of cheating, we use this as a global accum
        self.accum = []

    def find_all_rejected_paths(self):
        start = self.workflows['in']


    # start = workflow name
    # path = list of rules that brought us here
    def find_all_paths(self, start, path=[]):
        path = path + [start]
        paths = [path]
        if len(self.adjacency_list[start]) == 0:  # No neighbors, terminal state
            # check if its a rejected path
            if path[-1] == 'A':
                rules = self.path_to_rules(path)
                # print("[{}]".format(", ".join(rules)))

                # initially we accept everything
                accepted = {
                    'x': set(range(1, 4001)),
                    'm': set(range(1, 4001)),
                    'a': set(range(1, 4001)),
                    's': set(range(1, 4001))}
                
                # now take the intersection of whats accepted by each rule
                for r in rules:
                    # filter out default rules
                    if r.cmp:
                        prop, a_set = r.get_accepting_set() 
                        accepted[prop] = accepted[prop] & a_set

                print("finished processing rules. sizes as follows")
                for k, v in accepted.items():
                    print("{}: {}".format(k, len(v)))

                # accepted_for_path = prod([len(s) for s in accepted.values()])
                self.accum.append(accepted)
            # rules = self.path_to_rules(path)

        for workflow in self.adjacency_list[start]:
            newpaths = self.find_all_paths(workflow.name, path)
            for newpath in newpaths:
                paths.append(newpath)
        return paths
    
    def path_to_rules(self, path):
        r_path = []
        for w1_name, w2_name in itertools.pairwise(path):
            w1 = self.workflows[w1_name]
            for r in w1.rules:
                if r.dst == w2_name:
                    r_path.append(r)
                    break
        return r_path
    
    # ok so for each path that ends up at rejected, take the AND of every rule in the path.
    # then for each AND'ed list, OR those lists together.
    
    # no, i dont think this works: compute each path, one at a time. find the range of accepted 
    # for each path by mutiplying counts together, and sum the path counts together.

    # no, that doesnt work. take all the ANDs and OR them togther?

    # no, no, the deal is to sum the path ANDs together but avoid double counting, thats all

if __name__ == "__main__":
    f = open("input_day19_ex.txt", 'r')
    graph = Graph(f.readlines())
    graph.find_all_paths('in')

    accepted_map = graph.accum[0]
    # print(graph.accum[0])
    sys.exit(0)
    for a_map in graph.accum[1:]:
        for k, v in a_map.items():
            accepted_map[k] = accepted_map[k] | v

    acc = 1
    for k, v in accepted_map.items():
        print(len(v))
        acc *= len(v)

    print(acc)



    # for p in graph.find_all_paths('in'):
    #     # we gather all the rejected paths and use them to block off ranges
    #     # of the parameter space
    #     print(p)
    #     if p[-1] == 'R':
    #         rules = graph.path_to_rules(p)
    #         print(rules)
    #         sys.exit()