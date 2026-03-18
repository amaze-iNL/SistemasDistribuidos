from servidor.operacoes.dividir import Dividir
from servidor.operacoes.multiplicar import Multiplicar
from servidor.operacoes.somar import Somar
from servidor.operacoes.sqrt import Raizquadrada
from servidor.operacoes.subtrair import Subtrair


class Maquina:
    """
    Classe que processa os dados do cliente vindos da interface
    e executa as operações (através da respetiva classe).
    """
    def __init__(self):
        """
        Cria as instâncias e guarda os objetos de cada operação
        quando são criadas.
        """
        self.operacao_somar = Somar()
        self.operacao_subtrair = Subtrair()
        self.operacao_dividir = Dividir()
        self.operacao_sqrt = Raizquadrada()
        self.operacao_multiplicar = Multiplicar()

    def execute(self, operador, x, y):
        """

        :param operador: Símbolo da operação
        :param x: primeiro valor
        :param y: segundo valor (ignordo pela sqrt)
        :return:
            float - resultado do cálculo
            str - mensagem de erro
        """
        if operador == "+":
            return self.operacao_somar.executar(x, y)
        elif operador == "-":
            return self.operacao_subtrair.executar(x,y)
        elif operador == "*":
            return self.operacao_multiplicar.executar(x,y)
        elif operador == "/":
            return self.operacao_dividir.executar(x, y)
        elif operador == "sqrt":
            return self.operacao_sqrt.executar(x)

        else:
            return "Operação inválida"








