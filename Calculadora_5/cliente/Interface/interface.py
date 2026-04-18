import socket
import json
import cliente

class Interface:
    def __init__(self):
        self.connection = socket.socket()
        self.connection.connect((cliente.SERVER_ADDRESS, cliente.PORT))
        print(f"Ligado ao servidor em {cliente.SERVER_ADDRESS}:{cliente.PORT}")

    def send_str(self, value: str) -> None:
        self.connection.send(value.encode())

    def send_int(self, value: int, n_bytes: int) -> None:
        self.connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def receive_int(self, n_bytes: int) -> int:
        data = self.connection.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def send_object(self, obj):
        data = json.dumps(obj).encode('utf-8')
        size = len(data)
        self.send_int(size, cliente.INT_SIZE)
        self.connection.send(data)

    def execute(self):
        while True:
            print("\nEscolha a operação: + - * / sqrt (ou 'sair' para terminar)")
            operacao = input("Operação: ").strip().lower()

            if operacao == "sair":
                self.send_str(cliente.END_OP)
                self.connection.close()
                print("Conexão terminada.")
                break

            try:
                x = float(input("x = "))
                y = 0
                if operacao != "sqrt":
                    y = float(input("y = "))

                self.send_str(cliente.OBJ_OP)
                pedido = {
                    "oper": operacao,
                    "op1": x,
                    "op2": y
                }
                self.send_object(pedido)
                
                resultado = self.receive_int(cliente.INT_SIZE)
                print(f"Resultado: {resultado}")
            except ValueError:
                print("Erro: Introduza números válidos.")
            except Exception as e:
                print(f"Erro na comunicação: {e}")
                break

if __name__ == "__main__":
    ui = Interface()
    ui.execute()
