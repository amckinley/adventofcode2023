from enum import Flag, auto
import graphviz
from collections import deque

class Signal(Flag):
    LOW = False
    HIGH = True

class Module(object):
    def __init__(self, id: str):
        self.children = []
        self.id = id

    # turns the input signal and sender into an output decision
    def _handle(self, signal: Signal, sender) -> Signal:
        raise NotImplemented()
    
    def attach_child(self, mod):
        self.children.append(mod)

        # we need to tell Conj modules about all their inbound modules
        if type(mod) is Conj:
            mod.add_inbound(self)


class FlipFlop(Module):
    def __init__(self, id: str):
        super(FlipFlop, self).__init__(id)
        self.state = Signal.LOW
    
    def _handle(self, signal: Signal, sender) -> Signal:
        if signal == Signal.HIGH:
            return None
        else:
            self.state =  ~ self.state
            return self.state
        
    def to_spec(self) -> str:
        return "%{}".format(self.id)
    
class Conj(Module):
    def __init__(self, id: str):
        super(Conj, self).__init__(id)
        self.states = {}

    def _handle(self, signal: Signal, sender) -> Signal:
        # if we havent seen this sender before, set its state to LOW
        if sender.to_spec() not in self.states:
            print(self.states, sender.to_spec())
            raise Exception()
        # XXX: this might be a bug? maybe we need to initialize this list first?
        self.states[sender.to_spec()] = signal
    
        if all(self.states.values()):
            return Signal.LOW
        else:
            return Signal.HIGH
    
    def add_inbound(self, mod):
        self.states[mod.to_spec()] = Signal.LOW

    def to_spec(self) -> str:
        return "&{}".format(self.id)

class Broadcaster(Module):
    def __init__(self):
        super(Broadcaster, self).__init__('broadcaster')

    # we only ever get one signal, from the button module
    def _handle(self, signal: Signal, sender) -> Signal:
        return Signal.LOW
    
    def to_spec(self) -> str:
        return 'broadcaster'

class Button(Module):
    def __init__(self):
        super(Button, self).__init__('button')

    # we always send a LOW to the broadcaster
    def _handle(self, signal: Signal, sender) -> Signal:
        return Signal.LOW
    
    def to_spec(self) -> str:
        return 'button'
    
    def push(self):
        self.rx([])
    
class Output(Module):
    def __init__(self):
        super(Output, self).__init__('output')

    def _handle(self, signal: Signal, sender) -> Signal:
        return None
    
    def to_spec(self) -> str:
        return 'output'

class Machine(object):
    def __init__(self, lines):
        self.low_sent = 0
        self.high_sent = 0

        # first make all the objects
        spec_to_mod = {}
        id_to_mod = {}
        
        # implicit objects
        o = Output()
        spec_to_mod[o.to_spec()] = o
        id_to_mod[o.to_spec()] = o

        b = Button()
        self.button = b
        spec_to_mod[b.to_spec()] = b
        id_to_mod[b.to_spec()] = b
        
        for l in lines:
            name, _ = l.split(" -> ")
            if name == 'broadcaster':
                m = Broadcaster()
                self.broadcaster = m
            elif name.startswith('%'):
                name = name[1:]
                m = FlipFlop(name)
            elif name.startswith('&'):
                name = name[1:]
                m = Conj(name)
            else:
                raise Exception("unknown module {}".format(name))
            spec_to_mod[m.to_spec()] = m
            id_to_mod[name] = m

        # then attach children to them
        for l in lines:
            s_id, d_ids = l.split(" -> ")
            src = spec_to_mod[s_id]
            for d_id in d_ids.split(", "):
                dst = id_to_mod[d_id.strip()]
                src.attach_child(dst)

        # attach the button
        self.button.attach_child(id_to_mod['broadcaster'])

        self.spec_to_mod = spec_to_mod
        self.id_to_mod = id_to_mod

    def start(self, presses=1):
        for i in range(presses):
            # fake this out since we enqueue the first signal by hand
            # self.low_sent += 1
            self._run()

    def _run(self):
        to_send = deque()
        to_send.append((Signal.LOW, self.button, self.broadcaster))

        while len(to_send):
            signal, src, dst = to_send.popleft()
            output = dst._handle(signal, src)
            if signal == Signal.LOW:
                self.low_sent += 1
            elif signal == Signal.HIGH:
                self.high_sent += 1
            print("{} -{}-> {}\tq_len={}".format(src.id, signal, dst.id, len(to_send)))
            # self.print_q(to_send.copy())
            
            if output == None:
                continue
            
            for c in dst.children:
                to_send.append((output, dst, c))

    def print_q(self, q):
        for s, src, dst in q:
            print("\t{} -{}-> {}".format(src.to_spec(), s, dst.to_spec()))

        print()

    def png_out(self, filename='machine'):
        dot = graphviz.Digraph(format='png')
        for spec, m in self.spec_to_mod.items():
            dot.node(m.to_spec(), m.to_spec())
            for c in m.children:
                dot.edge(m.to_spec(), c.to_spec())
        dot.render(filename)

    def get_counts(self):
        print("low {} high {}".format(self.low_sent, self.high_sent))

if __name__ == "__main__":
    # f = FlipFlop("foo")
    # f.rx([Signal.LOW])
    # print(f.low_sent, f.high_sent)
    
    # s1 = Signal.HIGH
    # print(~ s1)
    # ss = [Signal.HIGH, Signal.HIGH, Signal.HIGH]
    # print(all(ss))
    # ss.append(Signal.LOW)
    # print(all(ss))

    f = open("input_day20_ex2.txt", 'r')
    m = Machine(f.readlines())
    m.start(presses=1000)
    m.get_counts()
    m.png_out()

