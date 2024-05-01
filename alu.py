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
