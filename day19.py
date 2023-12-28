import re

class Rule(object):
    def __init__(self, prop, cmp, val, dst):
        self.prop = prop
        self.cmp = cmp
        self.val = int(val)
        self.dst = dst

    # returns the ID of the workflow to send the part to if the rule matches, or None
    def pass_to(self, part):
        # print("in rule {}, trying part {}".format(self, part))
        prop_val = part.props[self.prop]
        if self.cmp == '>' and prop_val > self.val:
            return self.dst
        elif self.cmp == '<' and prop_val < self.val:
            return self.dst
        return None
    
    def __str__(self):
        return "[{}{}{}:{}]".format(self.prop, self.cmp, self.val, self.dst)
    
class DefaultRule(Rule):
    def __init__(self, dst):
        self.dst = dst

    def pass_to(self, part):
        return self.dst
    

class Part(object):
    def __init__(self, line):
        line = line[1:-1]
        values = line.split(',')
        props = {}
        for v in values:
            name, val = v.split('=')
            props[name] = int(val)
        self.props = props

    def __str__(self):
        return str(self.props)
    
    def score(self):
        return sum(self.props.values())

class Workflow(object):
    def __init__(self, line):
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

    def process_part(self, part):
        for r in self.rules:
            pass_to = r.pass_to(part)
            if pass_to:
                return pass_to
            
        # workflow doesnt handle this part
        raise Exception("how did i fail processing")
    
class Factory(object):
    def __init__(self, lines):
        workflow_lines = []
        part_lines = []
        in_workflows = True
        for l in lines:
            if l == '\n':
                in_workflows = False
                continue
            
            if in_workflows:
                workflow_lines.append(l.strip())
            else:
                part_lines.append(l.strip())

        workflows = {}
        for l in workflow_lines:
            w = Workflow(l)
            workflows[w.name] = w
        self.workflows = workflows

        parts = []
        for l in part_lines:
            p = Part(l)
            parts.append(p)
        self.parts = parts

    def get_accepted_score(self):
        sum = 0
        for p in self.parts:
            if self.process_part(p) == 'A':
                sum += p.score()

        return sum


    def process_part(self, part):
        path = []
        cur = 'in'
        while True:
            if cur in ['R', 'A']:
                break
            workflow = self.workflows[cur]
            next = workflow.process_part(part)
            path.append(cur)
            cur = next

        return cur


if __name__ == "__main__":
    f = open("input_day19.txt", 'r')
    factory = Factory(f.readlines())
    print(factory.get_accepted_score())