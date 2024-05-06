import basic


class Signal(basic.Signal):

    def __init__(self, sign_value: tuple = None):
        if sign_value is None:
            sign_value = basic.Signal.spawn(8)
        self._sign_value = sign_value

    @staticmethod
    def QuickCreate(value: int = 0):  #这玩意仅供测试，实际工作中要ban掉
        if value < 0 or value > 255:
            raise ValueError
        changed = "0" * 8 + bin(value)[2:]
        signal_list = []
        for single in changed[::-1]:  #从最低位置开始取
            signal = basic.Signal(int(single))
            signal_list.append(signal)
        return Signal(tuple(signal_list))


class Pin(basic.Pin):

    def __init__(self,
                 sign: Signal = Signal(),
                 target: list = None,
                 activity: bool = False,
                 lock: bool = False,
                 last: list = None):
        super().__init__(sign, target, activity, lock, last)
        self._sign = sign

    @staticmethod
    def spawn(num: int = 0):  #用于生成引脚
        list = []
        for i in range(num):
            pin = Pin()
            list.append(pin)
        return tuple(list)


class Splitter(basic.Element):

    def __init__(self, debug=False):
        in_pins = Pin.spawn(1)
        out_pins = basic.Pin.spawn(8)
        super().__init__(inpins=in_pins, outpins=out_pins, debug=debug)

    def logic(self):
        for index in range(8):
            self.outpins[index].write(self.inpins[0].read().read()[index])


class Combiner(basic.Element):

    def __init__(self, debug: bool = False):
        in_pins = basic.Pin.spawn(8)
        out_pins = Pin.spawn(1)
        super().__init__(inpins=in_pins, outpins=out_pins, debug=debug)

    def logic(self):
        sign_list = [sign.read() for sign in self.inpins]
        result = Signal(tuple(sign_list))
        self.outpins[0].write(result)


class And(basic.Element):

    def __init__(self, debug: bool = False):
        in_pins = Pin.spawn(2)
        out_pins = Pin.spawn(1)
        creator(basic.And, out_pins[0], in_pins)
        super().__init__(inpins=in_pins, outpins=out_pins, debug=debug)

    def logic(self):
        pass


class Or(basic.Element):

    def __init__(self, debug: bool = False):
        in_pins = Pin.spawn(2)
        out_pins = Pin.spawn(1)
        creator(basic.Or, out_pins[0], in_pins)
        super().__init__(inpins=in_pins, outpins=out_pins, debug=debug)

    def logic(self):
        pass


class Nand(basic.Element):

    def __init__(self, debug: bool = False):
        in_pins = Pin.spawn(2)
        out_pins = Pin.spawn(1)
        creator(basic.Nand, out_pins[0], in_pins)
        super().__init__(inpins=in_pins, outpins=out_pins, debug=debug)

    def logic(self):
        pass


class Nor(basic.Element):

    def __init__(self, debug: bool = False):
        in_pins = Pin.spawn(2)
        out_pins = Pin.spawn(1)
        creator(basic.Nor, out_pins[0], in_pins)
        super().__init__(inpins=in_pins, outpins=out_pins, debug=debug)

    def logic(self):
        pass


class Xor(basic.Element):

    def __init__(self, debug: bool = False):
        in_pins = Pin.spawn(2)
        out_pins = Pin.spawn(1)
        creator(basic.Xor, out_pins[0], in_pins)
        super().__init__(inpins=in_pins, outpins=out_pins, debug=debug)

    def logic(self):
        pass


class XNor(basic.Element):

    def __init__(self, debug: bool = False):
        in_pins = Pin.spawn(2)
        out_pins = Pin.spawn(1)
        creator(basic.XNor, out_pins[0], in_pins)
        super().__init__(inpins=in_pins, outpins=out_pins, debug=debug)

    def logic(self):
        pass


class Not(basic.Element):

    def __init__(self, debug: bool = False):
        gate_spl = Splitter()
        gate_comb = Combiner()
        gate_not_multi = basic.Element.spawn(basic.Not, 8)
        in_pins = Pin.spawn(1)
        out_pins = Pin.spawn(1)
        super().__init__(inpins=in_pins, outpins=out_pins, debug=debug)
        self.inpins[0].connect(gate_spl.inpins[0])
        for index in range(8):
            gate_spl.outpins[index].connect(gate_not_multi[index].inpins[0])
            gate_not_multi[index].outpins[0].connect(gate_comb.inpins[index])
        gate_comb.outpins[0].connect(self.outpins[0])

    def logic(self):
        pass


def creator(gate_class, out, inpins):  #用来创建与或等基本门
    splitters = basic.Element.spawn(Splitter, 2)
    gates = basic.Element.spawn(gate_class, 8)
    combiner = Combiner()
    for index in range(2):
        inpins[index].connect(splitters[index].inpins[0])
        for i in range(8):
            splitters[index].outpins[i].connect(gates[i].inpins[index])
            gates[i].outpins[0].connect(combiner.inpins[i])
    combiner.outpins[0].connect(out)


if __name__ == "__main__":
    spl = Splitter(debug=True)
    spl.inpins[0].write(Signal.QuickCreate(137))
    spl.inpins[0].work()
    while True:
        print(">>>", end="")
        try:
            exec(input())
        #except Exception as e:
        #    print(e)
        finally:
            pass
