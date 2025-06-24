import socket
import threading
from server.game_engine import GameEngine
from server.connection_manager import ConnectionManager


class MudServer:
    def __init__(self, host='0.0.0.0', port=4000):
        self.host = host
        self.port = port
        self.engine = GameEngine()
        self.manager = ConnectionManager(self.engine)

    def start(self):
        print(f"MUD 서버 실행 중... {self.host}:{self.port}")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen()

        try:
            while True:
                conn, addr = server_socket.accept()
                print(f"새 접속: {addr}")
                thread = threading.Thread(
                    target=self.manager.handle_client,
                    args=(conn, addr),
                    daemon=True
                )
                thread.start()
        except KeyboardInterrupt:
            print("서버를 종료합니다.")
        finally:
            server_socket.close()

if __name__ == '__main__':
    MudServer().start()
