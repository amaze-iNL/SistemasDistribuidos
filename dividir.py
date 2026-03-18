from typing import Union

class Dividir:
    def __init__(self):
        self.res = 0


    def executar(self, a:float, b:float)->Union[float,str]:
        try:
            self.res = a / b
        except ZeroDivisionError:
            return "Erro: Divisão por zero"
        return self.res