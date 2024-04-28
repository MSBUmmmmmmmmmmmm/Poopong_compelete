#Element的logic方法暂时只有几个低级原件在用，以后可能有别的用处
class Unactived(Exception):
    def __init__(self):
        super().__init__()

class Pin:
    
    def __init__(self, value:int=0, to:list=None, actived:bool=False):
        if to is None:
            to = []
        self.value = value
        self.actived = actived
        self.to = to

    def connect(self, obj):
        self.to.append(obj)

    def main(self):
        self.actived = True
        for obj in self.to:
            try:
                obj.value = self.value
            finally:
                obj.main()


class Element:

    def __init__(self, inpins:tuple=None, outpins:tuple=None):
        if inpins is None:
            inpins = ()
        if outpins is None:
            outpins = ()
        for i in inpins:
            i.connect(self)
        self.inpins = inpins
        self.outpins = outpins

    
    def main(self):
        try:
            for inpin in self.inpins:
                if not inpin.actived:
                    raise Unactived()
            self.logic()
            for outpin in self.outpins:
                outpin.main()
        except Unactived:
            pass

    def logic(self):
        pass

    

class Delay(Element):
    def __init__(self):
        in_pins = tuple([Pin()])
        out_pins = tuple([Pin()])
        super().__init__(inpins=in_pins, outpins=out_pins)
        self.stored = 0

    def logic(self):
        self.outpins[0].value = self.stored
        self.stored = self.inpins[0].value


class Not(Element):
    
    def __init__(self):
        in_pins = tuple([Pin()])
        out_pins = tuple([Pin()])
        super().__init__(inpins=in_pins, outpins=out_pins)

    def logic(self):
        self.outpins[0].value = 0
        if self.inpins[0].value == 0:
            self.outpins[0].value = 1

class And(Element):

    def __init__(self):
        in_pins = (Pin(), Pin())
        out_pins = tuple([Pin()])
        super().__init__(inpins=in_pins, outpins=out_pins)

    def logic(self):
        self.outpins[0].value = 0
        if self.inpins[0].value == 1:
            if self.inpins[1].value == 1:
                self.outpins[0].value = 1



class Nand(Element):
    
    def __init__(self):
        gate_and = And()
        gate_not = Not()
        in_pins = (Pin(), Pin())
        out_pins = tuple([Pin()])
        super().__init__(inpins=in_pins, outpins=out_pins)
        self.inpins[0].connect(gate_and.inpins[0])
        self.inpins[1].connect(gate_and.inpins[1])
        gate_and.outpins[0].connect(gate_not.inpins[0])
        gate_not.outpins[0].connect(self.outpins[0])



class Or(Element):
    
    def __init__(self):
        gate_not0 = Not()
        gate_not1 = Not()
        gate_nand = Nand()
        in_pins = (Pin(), Pin())
        out_pins = tuple([Pin()])
        super().__init__(inpins=in_pins, outpins=out_pins)
        self.inpins[0].connect(gate_not0.inpins[0])
        self.inpins[1].connect(gate_not1.inpins[0])
        gate_not0.outpins[0].connect(gate_nand.inpins[0])
        gate_not1.outpins[0].connect(gate_nand.inpins[1])
        gate_nand.outpins[0].connect(self.outpins[0])


class Nor(Element):
    def __init__(self):
        gate_or = Or()
        gate_not = Not()
        in_pins = (Pin(), Pin())
        out_pins = tuple([Pin()])
        super().__init__(inpins=in_pins, outpins=out_pins)
        self.inpins[0].connect(gate_or.inpins[0])
        self.inpins[1].connect(gate_or.inpins[1])
        gate_or.outpins[0].connect(gate_not.inpins[0])
        gate_not.outpins[0].connect(self.outpins[0])

class And3(Element):

    def __init__(self):
        in_pins = (Pin(), Pin(), Pin())
        out_pins = tuple([Pin()])
        gate_and0 = And()
        gate_and1 = And()
        super().__init__(inpins=in_pins, outpins=out_pins)
        self.inpins[0].connect(gate_and0.inpins[0])
        self.inpins[1].connect(gate_and0.inpins[1])
        gate_and0.outpins[0].connect(gate_and1.inpins[0])
        self.inpins[2].connect(gate_and1.inpins[1])
        gate_and1.outpins[0].connect(self.outpins[0])


class Or3(Element):

    def __init__(self):
        in_pins = (Pin(), Pin(), Pin())
        out_pins = tuple([Pin()])
        gate_or0 = Or()
        gate_or1 = Or()
        super().__init__(inpins=in_pins, outpins=out_pins)
        self.inpins[0].connect(gate_or0.inpins[0])
        self.inpins[1].connect(gate_or0.inpins[1])
        gate_or0.outpins[0].connect(gate_or1.inpins[0])
        self.inpins[2].connect(gate_or1.inpins[1])
        gate_or1.outpins[0].connect(self.outpins[0])


def TruthTable(gate_class):
    test_gate = gate_class()
    length = len(test_gate.inpins)
    situations = pow(2,length)
    print(f"Table name:{gate_class}")
    for i in range(situations):
        changed = "0"*length + bin(i)[2:]
        input_values = []
        for j in range(length):
            test_gate.inpins[j].value = int(changed[j-length])
            test_gate.inpins[j].main()
            input_values.append(test_gate.inpins[j].value)
        out_values = [k.value for k in test_gate.outpins]
        print(f"in:{input_values}, out:{out_values}")


if __name__ == "__main__":
    try:
        while True:
            exec(input())
    except Exception as e:
        print(e)
