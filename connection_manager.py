import threading

class ConnectionManager:
    def __init__(self, engine):
        self.engine = engine
        self.clients = {}

    def handle_client(self, conn, addr):
        conn.send("이름을 입력하세요: ".encode('utf-8'))
        name = conn.recv(1024).decode('utf-8').strip()
        welcome = self.engine.add_player(name)
        conn.send(f"{welcome}\n".encode('utf-8'))

        while True:
            try:
                conn.send("> ".encode('utf-8'))
                data = conn.recv(1024).decode('utf-8').strip()
                if not data or data.lower() == 'quit':
                    break
                response = self.engine.process_command(name, data)
                conn.send(f"{response}\n".encode('utf-8'))
            except:
                break

        conn.close()
