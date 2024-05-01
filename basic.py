# Element的logic方法暂时只有几个低级原件在用，以后可能有别的用处
class Inactivated(Exception):

    def __init__(self):
        super().__init__()


class Signal:

    def __init__(self, value: int = 0):
        if value != 0 and value != 1:
            raise ValueError
        self.sign = value


class Timer:

    def __init__(self, start: int = 0, step: int = 1):
        self.start = start
        self.step = step
        self._count = start

    def add(self):
        self._count += self.step

    def write(self, val: int):
        self._count = val

    def read(self):
        return self._count

    def reset(self):
        self.write(self.start)


class Pin:
    list_pins = []

    def __init__(self,
                 sign: Signal = Signal(0),
                 target: list = None,
                 activity: bool = False,
                 lock: bool = False,
                 last: list = None):
        if target is None:
            target = []
        if last is None:
            last = []
        if not isinstance(sign, Signal):
            raise TypeError
        if isinstance(sign.sign, tuple):
            sign = sign.sign[0]
        self._sign = sign
        self.activity = activity
        self.target = target
        self.last = last
        self.lock = lock
        Pin.list_pins.append(self)

    def connect(self, obj):
        self.target.append(obj)
        if isinstance(obj, Pin):
            obj.last.append(self)

    def work(self):
        self.activity = True
        self.lock = False
        try:
            for pin in self.last:
                if not pin.activity:
                    raise Inactivated()
            self.lock = False
            for obj in self.target:
                if isinstance(obj, Pin):
                    obj._sign = self._sign
                try:
                    obj.work()
                except Inactivated:
                    pass
        except Inactivated:
            self.lock = True

    def write(self, sign: Signal):
        self._sign = sign

    def read(self):
        return self._sign

    @staticmethod
    def reset():
        for pin in Pin.list_pins:
            pin.write(Signal(0))
            pin.activity = False
            pin.lock = False


class Element:

    def __init__(self, inpins: tuple = None, outpins: tuple = None):
        if inpins is None:
            inpins = ()
        if outpins is None:
            outpins = ()
        self.inpins = inpins
        self.outpins = outpins
        for pin in self.inpins:
            pin.connect(self)

    def work(self):
        try:
            for pin in self.inpins:
                if not pin.activity:
                    raise Inactivated()
            self.logic()
            for pin in self.outpins:
                pin.work()
        except Inactivated:
            pass

    def logic(self):
        print("So why a father needs to work personally??")
        pass


# Reg 中的inpins依次为写入，是否读，是否写
class Reg(Element):

    def __init__(self):
        super().__init__(inpins=tuple([Pin(), Pin(), Pin()]),
                         outpins=tuple([Pin()]))
        self._stored = Signal(0)

    def logic(self):
        self.outpins[0].write(Signal(0))
        if self.inpins[1]._sign == Signal(1):
            self.outpins[0].write(self.read())
        if self.inpins[2]._sign == Signal(1):
            self.write(self.inpins[0].read())

    def write(self, sign: Signal):
        self._stored = sign

    def read(self):
        return self._stored


class Not(Element):

    def __init__(self):
        in_pins = tuple([Pin()])
        out_pins = tuple([Pin()])
        super().__init__(inpins=in_pins, outpins=out_pins)

    def logic(self):
        self.outpins[0].write(Signal(0))
        if self.inpins[0].read() == Signal(0):
            self.outpins[0].write(Signal(1))


class And(Element):

    def __init__(self):
        in_pins = (Pin(), Pin())
        out_pins = tuple([Pin()])
        super().__init__(inpins=in_pins, outpins=out_pins)

    def logic(self):
        self.outpins[0].write(Signal(0))
        if self.inpins[0].read() == Signal(1):
            if self.inpins[1].read() == Signal(1):
                self.outpins[0].write(Signal(1))


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

    def logic(self):
        pass


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

    def logic(self):
        pass


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

    def logic(self):
        pass


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

    def logic(self):
        pass


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

    def logic(self):
        pass


def TruthTable(gate_class):
    test_gate = gate_class()
    length = len(test_gate.inpins)
    situations = pow(2, length)
    receive = [Pin()] * len(test_gate.outpins)
    print(receive)
    for index in range(len(test_gate.outpins)):
        test_gate.outpins[index].connect(receive[index])
    print(f"Table name:{gate_class}")
    for i in range(situations):
        changed = "0" * length + bin(i)[2:]
        input_values = []
        for j in range(length):
            test_gate.inpins[j].write(int(changed[j - length]))
            test_gate.inpins[j].work()
            input_values.append(test_gate.inpins[j].read())
        out_values = [pin.read().sign for pin in receive]
        print(f"in:{input_values}, out:{out_values}")
    Pin.reset()


if __name__ == "__main__":
    while True:
        print(">>>", end="")
        try:
            exec(input())
        except Exception as e:
            print(e)
