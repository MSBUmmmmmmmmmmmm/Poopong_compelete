import basic
from basic import TruthTable as TT1
import eight


class Half_adder(basic.Element):  #为什么变成异或门了啊啊啊 24.5.1 -MSBU 为什么它能跑了捏 5.2 M

    def __init__(self, debug: bool = False):
        gate_Xor = basic.Xor()
        gate_and = basic.And()
        in_pins = basic.Pin.spawn(2)
        out_pins = basic.Pin.spawn(2)
        super().__init__(inpins=in_pins, outpins=out_pins, debug=debug)
        self.inpins[0].connect(gate_and.inpins[0], gate_Xor.inpins[0])
        self.inpins[1].connect(gate_and.inpins[1], gate_Xor.inpins[1])
        gate_Xor.outpins[0].connect(self.outpins[0])
        gate_and.outpins[0].connect(self.outpins[1])

    def logic(self):
        pass


class Adder(basic.Element):

    def __init__(self, debug: bool = False):
        gate_half0 = Half_adder()
        gate_half1 = Half_adder()
        gate_or = basic.Or()
        in_pins = basic.Pin.spawn(3)
        out_pins = basic.Pin.spawn(2)
        super().__init__(inpins=in_pins, outpins=out_pins, debug=debug)
        self.inpins[0].connect(gate_half0.inpins[0])
        self.inpins[1].connect(gate_half0.inpins[1])
        gate_half0.outpins[0].connect(gate_half1.inpins[0])
        self.inpins[0].connect(gate_half1.inpins[1])
        gate_half1.outpins[0].connect(self.outpins[0])
        gate_half0.outpins[1].connect(gate_or.inpins[0])
        gate_half1.outpins[1].connect(gate_or.inpins[1])
        gate_or.outpins[0].connect(self.outpins[1])

    def logic(self):
        pass


if __name__ == "__main__":
    while True:
        print(">>>", end="")
        try:
            exec(input())
        #except Exception as e:
        #    print(e)
        finally:
            pass

import basic
from basic import TruthTable as TT1
import eight


class Half_adder(basic.Element):

    def __init__(self, debug: bool = False):
        gate_Xor = basic.Xor(debug=True)
        gate_and = basic.And()
        in_pins = basic.Pin.spawn(2)
        out_pins = basic.Pin.spawn(2)
        super().__init__(inpins=in_pins, outpins=out_pins, debug=debug)
        self.inpins[0].connect(gate_and.inpins[0], gate_Xor.inpins[0])
        self.inpins[1].connect(gate_and.inpins[1], gate_Xor.inpins[1])
        gate_Xor.outpins[0].connect(self.outpins[0])
        gate_and.outpins[0].connect(self.outpins[1])

    def logic(self):
        pass


if __name__ == "__main__":
    while True:
        print(">>>", end="")
        try:
            exec(input())
        #except Exception as e:
        #    print(e)
        finally:
            pass
