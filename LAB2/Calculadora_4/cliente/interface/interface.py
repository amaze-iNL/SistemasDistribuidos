import socket
import json


PORT = 35000
SERVER_ADDRESS = "192.168.1.75"
INT_SIZE = 8
COMMAND_SIZE = 9
ADD_OP = "add      "
SUB_OP = "sub      "
OBJ_OP = "add_obj  "
BYE_OP = "bye      "
END_OP = "stop     "



def send_str(connect, value: str) -> None:
    connect.send(value.encode())


def send_int(connect, value: int, n_bytes: int) -> None:
    connect.send(value.to_bytes(n_bytes, byteorder="big", signed=True))


def receive_int(connect, n_bytes: int) -> int:
    data = connect.recv(n_bytes)
    return int.from_bytes(data, byteorder='big', signed=True)


def send_object(connection, obj):
    """Serializa o objeto em JSON e envia (tamanho + dados)"""
    data = json.dumps(obj).encode('utf-8')
    size = len(data)
    send_int(connection, size, INT_SIZE)
    connection.send(data)


def receive_object(connection):
    """Recebe o tamanho e depois o objeto JSON desserializado"""
    size = receive_int(connection, INT_SIZE)
    data = connection.recv(size)
    return json.loads(data.decode('utf-8'))


class Interface:
    def __init__(self):
        # Estabelece a ligação no momento da inicialização
        self.connection = socket.socket()
        self.connection.connect((SERVER_ADDRESS, PORT))
        print(f"Ligado ao servidor remoto {SERVER_ADDRESS}:{PORT}")

    def execute(self):
        """Implementação da lógica de teste da Versão 3"""
        try:
            a, b = 10, 15
            print(f"\nTestando soma simples: {a} + {b}")
            send_str(self.connection, ADD_OP)
            send_int(self.connection, a, INT_SIZE)
            send_int(self.connection, b, INT_SIZE)
            res = receive_int(self.connection, INT_SIZE)
            print("Resultado:", res)

            print("\nTestando OBJ_OP com dicionário...")
            send_str(self.connection, OBJ_OP)
            pedido = {"oper": "+", "op1": a, "op2": b}
            send_object(self.connection, pedido)
            res_obj = receive_int(self.connection, INT_SIZE)
            print("Resultado OBJ_OP:", res_obj)

            for i in range(2):
                a += 1
                print(f"\nTestando subtração: {a} - {b}")
                send_str(self.connection, SUB_OP)
                send_int(self.connection, a, INT_SIZE)
                send_int(self.connection, b, INT_SIZE)
                res = receive_int(self.connection, INT_SIZE)
                print("Resultado:", res)

            print("\nA encerrar conexão...")
            send_str(self.connection, BYE_OP)

        except Exception as e:
            print(f"Erro durante a execução: {e}")
        finally:
            self.connection.close()



if __name__ == "__main__":
    ui = Interface()
    ui.execute()