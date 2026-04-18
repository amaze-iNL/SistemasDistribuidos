import socket
import servidor
from servidor.gestor.processa_cliente import ProcessaCliente

class Maquina:
    def __init__(self):
        self.s = socket.socket()
        self.s.bind(('', servidor.PORT))

    def execute(self):
        self.s.listen(5)
        print(f"Waiting for clients on port {servidor.PORT}")
        
        while True:
            print("On accept...")
            connection, address = self.s.accept()
            print(f"Client {address} connected")
            
            # Start thread for each client (Guide Part A requirement)
            processa = ProcessaCliente(connection, address)
            processa.start()

if __name__ == "__main__":
    maq = Maquina()
    maq.execute()
