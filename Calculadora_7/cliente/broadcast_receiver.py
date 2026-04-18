import threading
import json
import cliente

class BroadcastReceiver(threading.Thread):
    def __init__(self, connection):
        super().__init__(daemon=True)
        self.connection = connection

    def receive_int(self, n_bytes: int) -> int:
        data = self.connection.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def receive_object(self):
        size = self.receive_int(cliente.INT_SIZE)
        data = self.connection.recv(size)
        return json.loads(data.decode('utf-8'))

    def run(self):
        print("BroadcastReceiver active (every ~10s)")
        while True:
            try:
                hist = self.receive_object()
                print("\n[SERVER BROADCAST] Global history:")
                for oper, entries in hist.items():
                    print(f"  {oper}: {len(entries)} times")

                    for registo in entries:
                        a, b, resultado = registo[0], registo[1], registo[2]
                        print(f" -> {a} {oper} {b} = {resultado}")
                print("--------------------------------")
            except Exception:
                break
