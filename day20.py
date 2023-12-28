from enum import Flag, auto
import graphviz

class Signal(Flag):
    LOW = False
    HIGH = True

class Module(object):
    def __init__(self, id: str):
        self.children = []
        self.id = id
        self.low_sent = 0
        self.high_sent = 0
    
    def rx(self, signals: list[Signal]):
        # print("in an rx")
        output = self._handle(signals)
        # this module is not emitting a pulse
        if output == None:
            # print("no output, returning {}".format(self.id))
            return

        for c in self.children:
            if output == Signal.LOW:
                self.low_sent += 1
            elif output == Signal.HIGH:
                self.high_sent += 1
            else:
                raise Exception("bogus output {}".format(output))

            # print("{} -{}-> {}".format(self.to_spec(), output, c.to_spec()))
            # recursive call here will ensure that messages are fully processed by downstream
            # modules first
            c.rx([output])

    # turns the signals array into an output decision
    def _handle(self, signals: list[Signal]) -> Signal:
        raise NotImplemented()
    
    def attach_child(self, mod):
        self.children.append(mod)


class FlipFlop(Module):
    def __init__(self, id: str):
        super(FlipFlop, self).__init__(id)
        self.state = Signal.LOW
    
    def _handle(self, signals: list[Signal]) -> Signal:
        s = signals[0]
        if s == Signal.HIGH:
            return None
        else:
            self.state =  ~ self.state
            return self.state
        
    def to_spec(self) -> str:
        return "%{}".format(self.id)

    # def flipflop(state, r, s):
    #     return False if r else (True if s else state)
    
class Conj(Module):
    def __init__(self, id: str):
        super(Conj, self).__init__(id)
        self.states = []

    def _handle(self, signals: list[Signal]) -> Signal:
        for idx, s in enumerate(signals):
            self.states[idx] = s

        if all(self.states):
            return Signal.LOW
        else:
            return Signal.HIGH

    def attach_child(self, mod):
        super().attach_child(mod)
        self.states.append(Signal.LOW)

    def to_spec(self) -> str:
        return "&{}".format(self.id)

class Broadcaster(Module):
    def __init__(self):
        super(Broadcaster, self).__init__('broadcaster')

    # we only ever get one signal, from the button module
    def _handle(self, signals: list[Signal]) -> Signal:
        return signals[0]
    
    def to_spec(self) -> str:
        return 'broadcaster'

class Button(Module):
    def __init__(self):
        super(Button, self).__init__('button')

    def _handle(self, signals: list[Signal]) -> Signal:
        return Signal.LOW
    
    def to_spec(self) -> str:
        return 'button'
    
    def push(self):
        self.rx([])

    def _handle(self, signals: list[Signal]) -> Signal:
        return Signal.LOW
    
class Output(Module):
    def __init__(self):
        super(Output, self).__init__('output')

    def _handle(self, signals: list[Signal]) -> Signal:
        return None
    
    def to_spec(self) -> str:
        return 'output'

class Machine(object):
    def __init__(self, lines):
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
            self.button.push()


    def png_out(self, filename='machine'):
        dot = graphviz.Digraph(format='png')
        for spec, m in self.spec_to_mod.items():
            dot.node(m.to_spec(), m.to_spec())
            for c in m.children:
                dot.edge(m.to_spec(), c.to_spec())
        dot.render(filename)

    def get_counts(self):
        lows = 0
        highs = 0
        for m in self.id_to_mod.values():
            lows += m.low_sent
            highs += m.high_sent
        print("low {} high {}".format(lows, highs))

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

