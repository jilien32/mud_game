class GameEngine:
    def __init__(self):
        self.world = World()
        self.players = {}  # 접속 중인 유저
        self.user_manager = UserManager(FileUserRepository())

    def save_user_data(self, user_id):
        """사용자 위치, 소지품, 착용 장비 저장"""
        player = self.players.get(user_id)
        if player:
            # 예: 위치, 소지품, 착용 장비 등을 저장하는 로직
            # 여기서는 간단히 출력만 하지만, 실제로 파일이나 DB에 저장할 수 있음
            print(f"저장 중: {user_id} 위치({player.location}), 소지품({player.items}), 착용 장비({player.equipment})")
            # 실제 저장 작업 예시:
            # self.user_manager.save_user_state(user_id, player.location, player.items, player.equipment)

    def process_command(self, user_id, command):
        if user_id not in self.players:
            return "로그인이 필요합니다."

        player = self.players[user_id]
        if command == "끝":
            self.save_user_data(user_id)
            del self.players[user_id]
            return "로그아웃되었습니다. 게임을 종료합니다."
        elif command.startswith("이동 "):
            direction = command.split(" ")[1]
            return player.move(direction, self.world)
        elif command == "주변":
            room = self.world.get_room(player.location)
            return room.get('description', '')
        elif command == "상태":
            return (f"레벨: {player.level}\n"
                    f"체력: {player.hp['current']}/{player.hp['max']}\n"
                    f"마력: {player.mp['current']}/{player.mp['max']}\n"
                    f"스탯: {player.stats}")
        else:
            return "알 수 없는 명령어입니다."
        
    def process_command(self, user_id, command):
        if user_id not in self.players:
            return "로그인이 필요합니다."

        player = self.players[user_id]
        command = command.strip()

        if command == "끝":
            self.user_manager.save_player_state(user_id, player)
            del self.players[user_id]
            return "로그아웃되었습니다. 상태가 저장되었습니다."

        # 🧭 [보, 봐] → 현재 존 정보
        elif command in ("보", "봐"):
            room = self.world.get_room(player.location)
            return room.get("description", "이 지역은 설명이 없습니다.")

        # 🗡️ [공, 공격, 쳐] → 기본 공격
        elif command in ("공", "공격", "쳐"):
            damage = player.stats["힘"] * 2  # 임시 데미지 공식
            return f"당신은 기본 공격을 시도합니다! 데미지: {damage}"

        # 🧾 [상, 상태, 점, 점수, 정, 정보] → 상태창
        elif command in ("상", "상태", "점", "점수", "정", "정보"):
            return (
                f"📛 이름: {player.name}\n"
                f"📈 레벨: {player.level}\n"
                f"❤️ 체력: {player.hp['current']}/{player.hp['max']}\n"
                f"💙 마력: {player.mp['current']}/{player.mp['max']}\n"
                f"🧠 스탯:\n"
                f"   - 힘: {player.stats['힘']}\n"
                f"   - 민첩: {player.stats['민첩']}\n"
                f"   - 지능: {player.stats['지능']}\n"
                f"✨ 경험치: {player.exp}/{player.exp_to_level}\n"
                f"🧩 능력치 포인트: {player.stat_points}"
            )

        return "알 수 없는 명령어입니다."
