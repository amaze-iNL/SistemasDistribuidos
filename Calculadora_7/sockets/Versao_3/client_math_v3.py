import socket
import json
# PORT e SERVER ADDRESS

COMMAND_SIZE = 9
INT_SIZE = 8
ADD_OP = "add      "
OBJ_OP = "add_obj  "
SYM_OP = "sym      "
BYE_OP = "bye      "
SUB_OP = "sub      "
END_OP = "stop     "
PORT = 35000
SERVER_ADDRESS = "localhost"

# ----- enviar e receber strings ----- #
def receive_str(connect, n_bytes: int) -> str:
        """
        :param n_bytes: The number of bytes to read from the current connection
        :return: The next string read from the current connection
        """
        data = connect.recv(n_bytes)
        return data.decode()

def send_str(connect, value: str) -> None:

    connect.send(value.encode())

def send_int(connect:socket.socket, value: int, n_bytes: int) -> None:

    connect.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

def receive_int(connect: socket.socket, n_bytes: int) -> int:

        data = connect.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

def send_object(connection, obj):
 """1º: envia tamanho, 2º: envia dados."""
 data = json.dumps(obj).encode('utf-8')
 size = len(data)
 send_int(connection, size, INT_SIZE) # Envio do tamanho
 connection.send(data) # Envio do objeto
def receive_object(connection):
 """1º: lê tamanho, 2º: lê dados."""
 size = receive_int(connection, INT_SIZE) # Recebe o tamanho
 data = connection.recv(size) # Recebe o objeto
 return json.loads(data.decode('utf-8'))
def main():
    #Socket & ligação
    connection = socket.socket()
    connection.connect((SERVER_ADDRESS,PORT))
    # Testar a operação de soma
    a = 10
    b = 15
    send_str(connection,ADD_OP)
    send_int(connection,a, INT_SIZE)
    send_int(connection,b, INT_SIZE)
    res = receive_int(connection,INT_SIZE)
    print("O resultado da soma é:",res)
    # Execute a new type of operation: OBJ_OP
    print("\nA testar a operação OBJ_OP com um dicionário...")
    send_str(connection, OBJ_OP)

    pedido_dicionario = {"oper": "+", "op1": a, "op2": b}
    print(f"A enviar o dicionário: {pedido_dicionario}")
    send_object(connection, pedido_dicionario)

    res_obj = receive_int(connection, INT_SIZE)
    print("O resultado da soma de OBJ_OP é:", res_obj)
    # Client sends a dictionary.
    # Example: {"oper":"+","oper1":4,"oper2":5}
    # It receives an integer a result of the operation
    # ...
    # Testar duas operações de subtração
    for i in range(2):
        a += 1
        # Operação de subtração
        send_str(connection,SUB_OP)
        send_int(connection,a, INT_SIZE)
        send_int(connection,b, INT_SIZE)
        res = receive_int(connection,INT_SIZE)
        print("O resultado da subtração é:",res)
    # 1 Fechar a conexão apenas do lado do cliente ou...
    send_str(connection,BYE_OP)
    print("Connection is going to close...")
    #connection.close()
    # 2 Fechar a conexão do lado do cliente e do servidor
    #send_str(connection,END_OP)
    #connection.close()
    

if __name__=="__main__":
    main()
