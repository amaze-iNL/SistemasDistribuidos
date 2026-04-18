import threading
import servidor
import json
from servidor.operacoes.somar import Somar
from servidor.operacoes.subtrair import Subtrair

class ProcessaCliente(threading.Thread):
    def __init__(self, connection, address, dados):
        super().__init__()
        self.connection = connection
        self.address = address
        self.sum = Somar()
        self.dados = dados

    def receive_int(self, n_bytes: int) -> int:
        data = self.connection.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def send_int(self, value: int, n_bytes: int) -> None:
        self.connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def receive_str(self, n_bytes: int) -> str:
        data = self.connection.recv(n_bytes)
        return data.decode()

    def run(self):
        print(self.address, "Thread iniciada")
        last_request = False
        while not last_request:
            request_type = self.receive_str(servidor.COMMAND_SIZE)
            
            if request_type == servidor.ADD_OP:
                x = self.receive_int(servidor.INT_SIZE)
                y = self.receive_int(servidor.INT_SIZE)
                print(self.address, ":somar ", x, "+ ", y)
                result = self.sum.execute(x, y)
                self.send_int(result, servidor.INT_SIZE)
                # Regista soma
                self.dados.registar_oper('soma', x, y, result, self.address)
                print(self.address, ": registada uma soma")
            
            elif request_type == servidor.SUB_OP:
                x = self.receive_int(servidor.INT_SIZE)
                y = self.receive_int(servidor.INT_SIZE)
                # Not in guide but logical extension
                sub = Subtrair()
                result = sub.execute(x, y)
                self.send_int(result, servidor.INT_SIZE)
                self.dados.registar_oper('subtrair', x, y, result, self.address)
            
            elif request_type == servidor.END_OP:
                last_request = True
        
        print(self.address, "Thread terminada")
        print("Dicionario de dados:", self.dados.operacoes)
        self.connection.close()
