import socket
import json

from servidor.operacoes.dividir import Dividir
from servidor.operacoes.multiplicar import Multiplicar
from servidor.operacoes.somar import Somar
from servidor.operacoes.sqrt import Raizquadrada
from servidor.operacoes.subtrair import Subtrair

PORT = 35000
INT_SIZE = 8
COMMAND_SIZE = 9
OBJ_OP = "add_obj  "
END_OP = "stop     "

def receive_int(connection, n_bytes: int) -> int:
    data = connection.recv(n_bytes)
    return int.from_bytes(data, byteorder='big', signed=True)

def send_int(connection, value: int, n_bytes: int) -> None:
    connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

def receive_str(connection, n_bytes: int) -> str:
    data = connection.recv(n_bytes)
    return data.decode()

def receive_object(connection):
    size = receive_int(connection, INT_SIZE)
    data = connection.recv(size)
    return json.loads(data.decode('utf-8'))

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

    def ligar_server(self):
        s = socket.socket()
        s.bind(('', PORT))
        s.listen(1)
        print("Servidor da Calculadora 4 ligado!")

        keep_running = True
        while keep_running:
            # O servidor fica bloqueado até um cliente se ligar
            connection, address = s.accept()
            print(f"Cliente {address} acabou de se ligar!")

            last_request = False
            while not last_request:
                # Lê a string para saber o tipo de mensagem
                request_type = receive_str(connection, COMMAND_SIZE)

                if request_type == OBJ_OP:
                    #Recebe o dicionário com o pedido completo
                    pedido = receive_object(connection)
                    operador = pedido["oper"]
                    x = pedido["op1"]
                    y = pedido["op2"]
                    print(f"Pedido recebido do cliente: {x} {operador} {y}")

                    if operador == "+":
                        resultado = self.operacao_somar.executar(x, y)
                    elif operador == "-":
                        resultado =  self.operacao_subtrair.executar(x,y)
                    elif operador == "*":
                        resultado = self.operacao_multiplicar.executar(x,y)
                    elif operador == "/":
                        resultado = self.operacao_dividir.executar(x, y)
                    elif operador == "sqrt":
                        resultado = self.operacao_sqrt.executar(x)
                    else:
                        resultado = 0

                    if isinstance(resultado, str):
                        print(f"Erro no cálculo: {resultado}")
                        send_int(connection, 0, INT_SIZE)
                    else:
                        send_int(connection, int(resultado), INT_SIZE)


                elif request_type == END_OP:
                    print("O cliente terminou a ligação.")
                    last_request = True
                    keep_running = False  # Desliga o servidor

        s.close()
        print("Servidor desligado.")











