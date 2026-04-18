import threading
import servidor
import json
from servidor.operacoes.somar import Somar
from servidor.operacoes.subtrair import Subtrair
from servidor.operacoes.dividir import Dividir
from servidor.operacoes.multiplicar import Multiplicar
from servidor.operacoes.sqrt import Raizquadrada

class ProcessaCliente(threading.Thread):
    def __init__(self, connection, address):
        super().__init__()
        self.connection = connection
        self.address = address
        self.op_somar = Somar()
        self.op_subtrair = Subtrair()
        self.op_dividir = Dividir()
        self.op_multiplicar = Multiplicar()
        self.op_sqrt = Raizquadrada()

    def receive_int(self, connection, n_bytes: int) -> int:
        data = connection.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def send_int(self, connection, value: int, n_bytes: int) -> None:
        connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def receive_str(self, connection, n_bytes: int) -> str:
        data = connection.recv(n_bytes)
        return data.decode()

    def receive_object(self, connection):
        size = self.receive_int(connection, servidor.INT_SIZE)
        data = connection.recv(size)
        return json.loads(data.decode('utf-8'))

    def run(self):
        print(f"[{self.address}] Thread iniciada")
        last_request = False
        while not last_request:
            try:
                request_type = self.receive_str(self.connection, servidor.COMMAND_SIZE)
                if not request_type:
                    break
                
                if request_type == servidor.OBJ_OP:
                    pedido = self.receive_object(self.connection)
                    operador = pedido["oper"]
                    x = pedido["op1"]
                    y = pedido.get("op2", 0)

                    print(f"[{self.address}] Operação: {x} {operador} {y}")

                    if operador == "+":
                        resultado = self.op_somar.executar(x, y)
                    elif operador == "-":
                        resultado = self.op_subtrair.executar(x, y)
                    elif operador == "*":
                        resultado = self.op_multiplicar.executar(x, y)
                    elif operador == "/":
                        resultado = self.op_dividir.executar(x, y)
                    elif operador == "sqrt":
                        resultado = self.op_sqrt.executar(x)
                    else:
                        resultado = 0

                    self.send_int(self.connection, int(resultado), servidor.INT_SIZE)

                elif request_type == servidor.END_OP:
                    last_request = True
            except Exception as e:
                print(f"[{self.address}] Erro: {e}")
                break

        print(f"[{self.address}] Thread terminada")
        self.connection.close()