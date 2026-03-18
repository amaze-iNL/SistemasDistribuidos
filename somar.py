from typing import Union


class Somar:
    def __init__(self):
        self.res = 0

    def executar(self, a:float, b:float)->Union[float,str]:
        self.res = a + b
        return self.res

