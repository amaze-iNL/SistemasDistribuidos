import threading
import servidor
import json
from servidor.operacoes.somar import Somar
from servidor.operacoes.subtrair import Subtrair
from servidor.operacoes.dividir import Dividir
from servidor.operacoes.multiplicar import Multiplicar
from servidor.operacoes.sqrt import Raizquadrada

class ProcessaCliente(threading.Thread):
    def __init__(self, connection, address, lista_clientes, dados):
        super().__init__()
        self.connection = connection
        self.address = address
        self.lista_clientes = lista_clientes
        self.dados = dados
        
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
        # Register client
        self.lista_clientes.adicionar(self.address, self.connection)
        print(f"[{self.address}] Thread iniciada")
        
        last_request = False
        while not last_request:
            try:
                request_type = self.receive_str(self.connection, servidor.COMMAND_SIZE)
                if not request_type:
                    break
                
                # AGORA SIM: Aceita o '+' ou '-' que o teu cliente envia!
                if request_type == servidor.ADD_OP or request_type == "+":
                    x = self.receive_int(self.connection, servidor.INT_SIZE)
                    y = self.receive_int(self.connection, servidor.INT_SIZE)
                    print(f"[{self.address}] Operação: {x} + {y}")
                    resultado = self.op_somar.executar(x, y)
                    self.dados.registar_oper('+', x, y, resultado, self.address)
                    
                elif request_type == servidor.SUB_OP or request_type == "-":
                    x = self.receive_int(self.connection, servidor.INT_SIZE)
                    y = self.receive_int(self.connection, servidor.INT_SIZE)
                    print(f"[{self.address}] Operação: {x} - {y}")
                    resultado = self.op_subtrair.executar(x, y)
                    self.dados.registar_oper('-', x, y, resultado, self.address)

                elif request_type == servidor.END_OP:
                    last_request = True
            except Exception as e:
                print(f"[{self.address}] Erro: {e}")
                break

        # Unregister client
        self.lista_clientes.remover(self.address)
        print(f"[{self.address}] Thread terminada")
        self.connection.close()
