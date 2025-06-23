import socket
from .game_engine import GameEngine
from .connection_manager import ConnectionManager

HOST = '127.0.0.1'
PORT = 4000

def run_server():
    engine = GameEngine()
    manager = ConnectionManager(engine)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("서버 실행 중...")

        while True:
            conn, addr = s.accept()
            print(f"{addr} 접속됨.")
            thread = threading.Thread(target=manager.handle_client, args=(conn, addr))
            thread.start()
