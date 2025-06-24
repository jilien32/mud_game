from server.world import World
from server.user_manager import UserManager
from server.user_repository import FileUserRepository
from server.player import Player
from server.chat_manager import ChatManager

def recv_line(conn):
    buffer = b""
    while True:
        chunk = conn.recv(1)
        if not chunk:
            return None  # 연결 종료
        if chunk in [b'\r', b'\n']:
            break
        buffer += chunk

    # CRLF 연속 처리
    conn.setblocking(False)
    try:
        while True:
            next_byte = conn.recv(1)
            if next_byte not in [b'\r', b'\n']:
                break
    except:
        pass
    conn.setblocking(True)

    return buffer.decode("cp949", errors="ignore").strip()

class GameEngine:
    def __init__(self):
        self.world = World()
        self.players = {}
        self.user_manager = UserManager(FileUserRepository())
        self.chat_manager = ChatManager(self.players)

    def handle_login(self, conn):
        try:
            # 인트로 메시지
            intro = [
                "-" * 50,
                "100년 전... 데이모스의 부활",
                "",
                "암흑의 시대, 죽음의 탑에서 벌어진 전쟁은",
                "미스타라 대륙을 폐허로 만들었습니다.",
                "그리고 잊혀진 예언 속 왕관이 다시 깨어납니다...",
                "",
                "-" * 50,
                "현재 접속 중인 모험가들:",
                ""
            ]
            if self.players:
                for uid, p in self.players.items():
                    intro.append(f"  - {uid} (레벨 {p.level}, {p.kingdom})")
            else:
                intro.append("  - 아무도 없습니다. 당신이 첫 번째입니다!")

            for line in intro:
                conn.sendall((line + "\r\n").encode("cp949", errors="ignore"))

            # 사용자 이름 입력
            while True:
                conn.sendall("사용자 이름: ".encode("cp949"))
                user_id = recv_line(conn)
                if not user_id:
                    conn.sendall("아이디를 입력하지 않아 접속을 종료합니다.\r\n".encode("cp949"))
                    return None
                if user_id.strip():
                    break
                conn.sendall("아이디는 빈 값일 수 없습니다.\r\n".encode("cp949"))

            # 중복 로그인 처리
            if user_id in self.players:
                old_player = self.players[user_id]
                if hasattr(old_player, 'conn') and old_player.conn:
                    try:
                        old_player.conn.sendall("다른 곳에서 접속하여 연결이 종료됩니다.\r\n".encode("cp949"))
                        old_player.conn.close()
                    except:
                        pass
                del self.players[user_id]

            # 신규 유저 여부 확인
            if user_id not in self.user_manager.users:
                while True:
                    conn.sendall("존재하지 않는 아이디입니다. 새로 가입하시겠습니까? (네/아니오): ".encode("cp949"))
                    confirm = recv_line(conn)
                    if not confirm:
                        return None
                    confirm = confirm.lower()
                    if confirm == "네":
                        while True:
                            conn.sendall("비밀번호를 입력하세요: ".encode("cp949"))
                            password = recv_line(conn)
                            if not password:
                                conn.sendall("비밀번호는 빈 값일 수 없습니다.\r\n".encode("cp949"))
                                continue
                            ok, msg = self.user_manager.register(user_id, password)
                            conn.sendall((msg + "\r\n").encode("cp949"))
                            if not ok:
                                return None
                            break
                        break
                    elif confirm == "아니오":
                        conn.sendall("접속을 종료합니다.\r\n".encode("cp949"))
                        return None
                    else:
                        conn.sendall("네 또는 아니오로 입력해주세요.\r\n".encode("cp949"))

            # 비밀번호 입력
            while True:
                conn.sendall("비밀번호: ".encode("cp949"))
                password = recv_line(conn)
                if not password:
                    conn.sendall("비밀번호는 빈 값일 수 없습니다.\r\n".encode("cp949"))
                    continue
                ok, msg = self.user_manager.login(user_id, password)
                conn.sendall((msg + "\r\n").encode("cp949"))
                if ok:
                    break
                else:
                    return None

            # 유저 상태 불러오기
            state = self.user_manager.load_player_state(user_id)
            if "location" in state:
                x, y, z = state.pop("location")
                state["x"], state["y"], state["z"] = x, y, z

            player = Player.load_data(user_id, state)
            player.conn = conn
            self.players[user_id] = player

            conn.sendall(f"{user_id}님, 접속을 환영합니다!\r\n".encode("cp949"))
            return user_id

        except Exception as e:
            conn.sendall(f"로그인 중 오류 발생: {str(e)}\r\n".encode("cp949", errors="ignore"))
            return None
        
        finally:
            conn.sendall("\x1b[2J\x1b[H".encode())  # 화면 클리어
            for line in intro:
                conn.sendall((line + "\r\n").encode("cp949", errors="ignore"))


    def save_user_data(self, user_id):
        """사용자 위치, 소지품, 착용 장비 저장"""
        player = self.players.get(user_id)
        if player:
            # 예: 위치, 소지품, 착용 장비 등을 저장하는 로직
            # 여기서는 간단히 출력만 하지만, 실제로 파일이나 DB에 저장할 수 있음
            print(f"저장 중: {user_id} 위치({player.get_location}), 소지품({player.items}), 착용 장비({player.equipment})")
            # 실제 저장 작업 예시:
            # self.user_manager.save_user_state(user_id, player.location, player.items, player.equipment)

    # game_engine.py

# ... (기존 코드)

    def process_command(self, user_id, command):
        if user_id not in self.players:
            return "로그인이 필요합니다."

        player = self.players[user_id]
        command = command.strip()

        if command == "끝":
            self.user_manager.save_player_state(user_id, player)
            del self.players[user_id]
            return "로그아웃되었습니다. 상태가 저장되었습니다."

        words = command.split()
        if not words:
            return "" # 빈 명령어는 무시

        # 채팅 명령어 처리
        if len(words) > 1:
            # "메시지 말" 형식의 채팅 명령어
            last_word = words[-1]
            message = " ".join(words[:-1])
            if last_word in ("말", "말하기"):
                return self.chat_manager.chat_room(user_id, message)
            elif last_word in ("그", "그룹말"):
                return self.chat_manager.chat_group(user_id, message)
            elif last_word in ("잡", "잡담"):
                return self.chat_manager.chat_global(user_id, message)
            # "[대상이름] 메시지 속" 형식의 귓속말
            elif words[-1] == "속" and len(words) >= 3:
                target_id = words[0]
                message = " ".join(words[1:-1])
                return self.chat_manager.chat_whisper(user_id, target_id, message)

        # 게임 관련 명령어 처리
        if command in ("누", "누구"):
            return self.list_players()
        elif command in ("상", "상태", "점", "점수", "정", "정보"):
            return self.get_status(player) # get_status 함수 구현 필요
        elif command in ("보", "봐"):
            room = self.world.get_room(player.get_location)
            exits = ", ".join(room["exits"].keys())
            players_in_room = [name for name, p in self.players.items() if p.get_location == player.get_location and name != user_id]
            
            response = f"--- {room.get('name', '???')} ---\n"
            response += f"{room.get('description', '')}\n"
            response += f"이동 가능한 방향: {exits}\n"
            if players_in_room:
                response += f"다른 플레이어: {', '.join(players_in_room)}"
            return response
            
        elif command in ("지", "지도"):
            return self.get_minimap(player)

        # 이동 명령어
        elif command in ("ㄷ", "동", "ㅅ", "서", "ㅂ", "북", "ㄴ", "남", "ㅄ", "북서", "ㅂㄷ", "북동",
                 "ㄴㅅ", "남서", "ㄴㄷ", "남동", "ㅇ", "위", "ㅁ", "밑"):

            direction_map = {
                "ㄷ": "동", "동": "동", "ㅅ": "서", "서": "서", "ㅂ": "북", "북": "북", "ㄴ": "남", "남": "남",
                "ㅄ": "북서", "북서": "북서", "ㅂㄷ": "북동", "북동": "북동", "ㄴㅅ": "남서", "남서": "남서",
                "ㄴㄷ": "남동", "남동": "남동", "ㅇ": "위", "위": "위", "ㅁ": "밑", "밑": "밑"
            }

            direction = direction_map[command]
            
            # 위치를 읽을 때 반드시 get_location으로 호출
            current_pos = player.get_location
            current_room = self.world.get_room(current_pos)
            
            if direction not in current_room["exits"]:
                return f"그 방향({direction})으로는 이동할 수 없습니다."

            new_pos = current_room["exits"][direction]

            # 위치를 변경할 때는 반드시 set_location 사용
            player.set_location(*new_pos)
            
            room = self.world.get_room(player.get_location)
            exits = ", ".join(room["exits"].keys())
            return (
                f"{room['description']}\n"
                f"좌표: {player.get_location}\n"
                f"이동 가능한 방향: {exits}"
            )

        return "알 수 없는 명령어입니다. [도움말]을 입력해보세요."

    def get_status(self, player):
        # 플레이어 상태를 보여주는 상세 정보
        return (f"--- {player.user_id}님의 상태 ---\n"
                f"레벨: {player.level} (경험치: {player.exp}/100)\n"
                f"체력: {player.hp} / {100 + player.str * 10}\n"
                f"마력: {player.mp} / {50 + player.int * 10}\n"
                f"힘: {player.str}\n"
                f"민첩: {player.dex}\n"
                f"지능: {player.int}\n"
                f"소지품: {player.inventory}\n"
                f"장착: {player.equipped}\n"
                f"왕국: {player.kingdom}\n"
                f"보유 스탯 포인트: {player.stat_points}")

    def get_minimap(self, player):
        cx, cy, cz = player.get_location
        size = 2  # 위아래/좌우 2칸 (5×5)
        lines = ["주변 5x5 지역 미니맵"]

        for dy in range(size, -size - 1, -1):  # y축은 위에서 아래로
            row = []
            for dx in range(-size, size + 1):
                pos = (cx + dx, cy + dy, cz)
                if pos == player.get_location:
                    row.append("나")  # 나 (현재 위치)
                elif pos in self.world.rooms:
                    room = self.world.get_room(pos)
                    room_name = room.get("name", "???")[:2]
                    row.append(f" {room_name}")
                else:
                    row.append(" ..")
            lines.append(" | ".join(row))
        return "\n".join(lines)

    