import socket
import cliente

class Interface:
    def __init__(self):
        self.connection = socket.socket()
        self.connection.connect((cliente.SERVER_ADDRESS, cliente.PORT))
        print(f"Connected to server at {cliente.SERVER_ADDRESS}:{cliente.PORT}")

    def send_str(self, value: str) -> None:
        self.connection.send(value.encode())

    def send_int(self, value: int, n_bytes: int) -> None:
        self.connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def receive_int(self, n_bytes: int) -> int:
        data = self.connection.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def execute(self):
        while True:
            print("\nSelect operation: + - (or 'stop' to exit)")
            op = input("Op: ").strip().lower()

            if op == "stop":
                self.send_str(cliente.END_OP)
                self.connection.close()
                print("Exiting...")
                break
            
            try:
                x = int(input("x = "))
                y = int(input("y = "))

                if op == "+":
                    self.send_str(cliente.ADD_OP)
                elif op == "-":
                    self.send_str(cliente.SUB_OP)
                else:
                    print("Invalid op.")
                    continue

                self.send_int(x, cliente.INT_SIZE)
                self.send_int(y, cliente.INT_SIZE)
                res = self.receive_int(cliente.INT_SIZE)
                print(f"Result: {res}")
            except ValueError:
                print("Error: numbers only.")

if __name__ == "__main__":
    ui = Interface()
    ui.execute()
