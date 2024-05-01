import basic


class Signal(basic.Signal):

    def __init__(self, signal: tuple = None):
        if signal is None:
            signal = tuple([basic.Signal(0)] * 8)
        self.sign = signal


class Pin(basic.Pin):

    def __init__(self,
                 sign: Signal = Signal(),
                 target: list = None,
                 activity: bool = False,
                 lock: bool = False,
                 last: list = None):
        print(sign)
        super().__init__(sign, target, activity, lock, last)
        self._sign = sign


class Splitter(basic.Element):

    def __init__(self):
        in_pins = tuple([Pin()])
        out_pins = tuple([basic.Pin()] * 8)
        super().__init__(inpins=in_pins, outpins=out_pins)

    def logic(self):
        map(lambda x, y: x.write(y.read()), self.outpins, self.inpins._sign)


if __name__ == "__main__":
    while True:
        print(">>>", end="")
        try:
            exec(input())
        #except Exception as e:
        #    print(e)
        finally:
            pass
