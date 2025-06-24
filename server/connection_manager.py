import traceback

class ConnectionManager:
    def __init__(self, engine):
        self.engine = engine
        self.clients = {}  # conn → user_id

    def handle_client(self, conn, addr):
        print(f"{addr} 연결됨.")
        try:
            user_id = self.engine.handle_login(conn)
            if not user_id:
                conn.close()
                return

            self.clients[conn] = user_id
            conn.sendall(f"{user_id}님, 환영합니다!\r\n".encode('cp949'))

            while True:
                data = conn.recv(2048)
                if not data:
                    break

                message = data.decode('cp949', errors='ignore').strip()
                if not message:
                    continue

                response = self.engine.process_command(user_id, message)
                player = self.engine.players.get(user_id)
                prompt = f"\r\n← {player.hp}체력, {player.mp}마력 → "

                if message == "끝":
                    if response:
                        conn.sendall((response + prompt).encode('cp949'))
                    break

                if isinstance(response, list):
                    for target_id, msg in response:
                        target_conn = self.get_conn_by_user_id(target_id)
                        if target_conn:
                            target_conn.sendall((msg + "\r\n").encode('cp949'))
                    conn.sendall(("메시지를 보냈습니다." + prompt).encode('cp949'))
                else:
                    conn.sendall((response + prompt).encode('cp949'))

        except Exception as e:
            print(f"에러 발생: {e}")
            traceback.print_exc()
        finally:
            if conn in self.clients:
                del self.clients[conn]
            conn.close()
            print(f"{addr} 연결 종료됨.")


    def get_conn_by_user_id(self, user_id):
        for conn, uid in self.clients.items():
            if uid == user_id:
                return conn
        return None
