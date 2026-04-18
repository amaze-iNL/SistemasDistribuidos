import socket
import servidor
from servidor.gestor.processa_cliente import ProcessaCliente
from servidor.gestor.lista_clientes import ListaClientes
from servidor.gestor.thread_broadcast import ThreadBroadcast
from servidor.dados.dados import Dados

class Maquina:
    def __init__(self):
        self.s = socket.socket()
        self.s.bind(('', servidor.PORT))
        self.lista_clientes = ListaClientes()
        self.dados = Dados()
        
        # Start Broadcast Thread
        self.broadcast = ThreadBroadcast(self.lista_clientes, self.dados, intervalo=10)
        self.broadcast.start()

    def execute(self):
        self.s.listen(5)
        print(f"Servidor Calculadora 7 ligado na porta {servidor.PORT}")
        
        while True:
            connection, address = self.s.accept()
            print(f"Cliente {address} conectado")
            
            # Create thread with shared state
            processa = ProcessaCliente(connection, address, self.lista_clientes, self.dados)
            processa.start()

if __name__ == "__main__":
    maq = Maquina()
    maq.execute()
