import threading

class ConnectionManager:
    def __init__(self, engine):
        self.engine = engine
        self.logged_in_users = set()  # 로그인된 유저를 추적하는 세션 관리 (중복 로그인 방지)

    def handle_client(self, conn, addr):
        print(f"{addr} 연결됨.")
        try:
            user_id = self.engine.handle_login(conn)
            
            # 중복 로그인 방지
            if not user_id:
                conn.send("로그인에 실패했습니다. 다시 시도해주세요.\n".encode('utf-8'))
                conn.close()
                print(f"{addr} 로그인 실패로 연결 종료.")
                return

            if user_id in self.logged_in_users:
                conn.send("이미 로그인된 사용자입니다. 게임을 종료합니다.\n".encode('utf-8'))
                conn.close()
                print(f"{addr} 중복 로그인 시도 종료.")
                return

            self.logged_in_users.add(user_id)  # 로그인된 유저로 추가
            conn.send(f"{user_id}님, 환영합니다!\n".encode('utf-8'))

            while True:
                conn.send("> ".encode('utf-8'))
                data = conn.recv(1024).decode('utf-8').strip()
                if not data:
                    break

                response = self.engine.process_command(user_id, data)

                # "끝" 명령어 처리: 로그아웃 시 상태 저장
                if data == "끝":
                    self.engine.save_user_data(user_id)  # 위치, 소지품, 착용 장비 저장
                    self.logged_in_users.remove(user_id)  # 중복 로그인 방지를 위해 로그아웃 처리
                    conn.send("로그아웃되었습니다. 게임을 종료합니다.\n".encode('utf-8'))
                    print(f"{user_id}님이 로그아웃했습니다.")
                    break

                conn.send((response + "\n").encode('utf-8'))

        except Exception as e:
            print(f"오류 발생: {e}")
        finally:
            conn.close()
            print(f"{addr} 연결 종료됨.")
