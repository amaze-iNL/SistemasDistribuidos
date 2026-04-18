import socket
import servidor
from servidor.processa_cliente import ProcessaCliente
from servidor.dados.dados import Dados
from servidor.operacoes.somar import Somar

class Maquina:
    def __init__(self):
        self.sum = Somar()
        self.dados = Dados()
        self.s = socket.socket()
        self.s.bind(('', servidor.PORT))

    def execute(self):
        self.s.listen(5)
        print("Waiting for clients on port " + str(servidor.PORT))
        
        while True:
            print("On accept...")
            connection, address = self.s.accept()
            print("Client", address, "connected")
            
            processo_cliente = ProcessaCliente(connection, address, self.dados)
            processo_cliente.start()

if __name__ == "__main__":
    maq = Maquina()
    maq.execute()
