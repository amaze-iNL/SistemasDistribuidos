from typing import Union


class Raizquadrada:
    def __init__(self):
        self.res = 0

    def executar(self, a:float)->Union[float,str]:
        self.res= a ** 0.5
        return self.res
