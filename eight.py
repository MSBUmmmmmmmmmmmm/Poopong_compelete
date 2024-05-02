import basic


class Signal(basic.Signal):

    def __init__(self, signal: tuple = None):
        if signal is None:
            signal = tuple([basic.Signal(0)] * 8)
        self._sign_value = signal


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

    @staticmethod
    def spawn(num: int = 0):  #用于生成引脚
        list = []
        for i in range(num):
            pin = Pin()
            list.append(pin)
        return tuple(list)


class Splitter(basic.Element):

    def __init__(self):
        in_pins = tuple([Pin()])
        out_pins = tuple([basic.Pin()] * 8)
        super().__init__(inpins=in_pins, outpins=out_pins)

    def logic(self):
        map(lambda x, y: x.write(y.read()), self.outpins, self.inpins[0]._sign)


if __name__ == "__main__":
    while True:
        print(">>>", end="")
        try:
            exec(input())
        #except Exception as e:
        #    print(e)
        finally:
            pass


class Signal(basic.Signal):

    def __init__(self, signal: tuple = None):
        if signal is None:
            signal = tuple([basic.Signal(0)] * 8)
        self._sign_value = signal


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

    @staticmethod
    def spawn(num: int = 0):  #用于生成引脚
        list = []
        for i in range(num):
            pin = Pin()
            list.append(pin)
        return tuple(list)


class Splitter(basic.Element):

    def __init__(self):
        in_pins = tuple([Pin()])
        out_pins = tuple([basic.Pin()] * 8)
        super().__init__(inpins=in_pins, outpins=out_pins)

    def logic(self):
        map(lambda x, y: x.write(y.read()), self.outpins, self.inpins[0]._sign)


if __name__ == "__main__":
    while True:
        print(">>>", end="")
        try:
            exec(input())
        #except Exception as e:
        #    print(e)
        finally:
            pass
