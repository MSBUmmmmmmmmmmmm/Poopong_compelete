from eight import *


def TestSplitter(in_value: int):
    spl = Splitter()
    spl.inpins[0].write(Signal.QuickCreate(in_value))
    spl.inpins[0].work()
    print(bin(in_value))


def TestNot(in0):
    gate = Not()
    gate.inpins[0].write(Signal.QuickCreate(in0))
    gate.inpins[0].work()
    out = [sign.read() for sign in gate.outpins[0].read().read()]
    print(f"out:{out}")
    print(bin(in0))


def TestBasicGates(gate_class, in0, in1):
    gate = gate_class()
    gate.inpins[0].write(Signal.QuickCreate(in0))
    gate.inpins[0].work()
    gate.inpins[1].write(Signal.QuickCreate(in1))
    gate.inpins[1].work()
    out = [sign.read() for sign in gate.outpins[0].read().read()]
    print(f"out:{out}")
    print(bin(in0))
    print(bin(in1))


if __name__ == "__main__":
    while True:
        print(">>>", end="")
        try:
            exec(input())
        #except Exception as e:
        #    print(e)
        finally:
            pass
