import socket
import cliente
from cliente.broadcast_receiver import BroadcastReceiver

class Interface:
    def __init__(self):
        self.connection = socket.socket()
        self.connection.connect((cliente.SERVER_ADDRESS, cliente.PORT))
        print(f"Connected to {cliente.SERVER_ADDRESS}:{cliente.PORT}")
        
        # Start receiver thread (Guide B, III.E)
        self.receiver = BroadcastReceiver(self.connection)
        self.receiver.start()

    def send_str(self, value: str) -> None:
        self.connection.send(value.encode())

    def send_int(self, value: int, n_bytes: int) -> None:
        self.connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def receive_int(self, n_bytes: int) -> int:
        data = self.connection.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def execute(self):
        while True:
            print("\nCalc (+ or -) / 'stop' to end")
            op = input("Op: ").strip().lower()

            if op == "stop":
                self.send_str(cliente.END_OP)
                self.connection.close()
                break
            
            try:
                x = int(input("x = "))
                y = int(input("y = "))
                if op == "+": self.send_str(cliente.ADD_OP)
                elif op == "-": self.send_str(cliente.SUB_OP)
                else: continue
                
                self.send_int(x, cliente.INT_SIZE)
                self.send_int(y, cliente.INT_SIZE)

                # res = self.receive_int(cliente.INT_SIZE)
                # print(f"Result: {res}")
                print("Operação enviada. Aguarda o broadcast...")
            except Exception:
                break

if __name__ == "__main__":
    ui = Interface()
    ui.execute()
