class UserManager:
    def __init__(self, repository):
        self.repository = repository
        self.users = self.repository.load_users()

    def register(self, user_id, password):
        if user_id in self.users:
            return False, "이미 존재하는 아이디입니다."
        self.users[user_id] = {'password': password}
        self.repository.save_users(self.users)
        return True, "회원가입 완료."

    def login(self, user_id, password):
        if user_id not in self.users:
            return False, "존재하지 않는 아이디입니다."
        if self.users[user_id]['password'] != password:
            return False, "비밀번호가 틀렸습니다."
        return True, "로그인 성공."

    def save(self):
        self.repository.save_users(self.users)

    def save_player_state(self, user_id, player: Player):
        if user_id in self.users:
            self.users[user_id].update(player.to_dict())
            self.repository.save_users(self.users)

    def load_player_state(self, user_id):
        user_data = self.users.get(user_id, {})
        return {
            "location": user_data.get("location", "start"),
            "inventory": user_data.get("inventory", []),
            "equipment": user_data.get("equipment", {"무기": None, "방어구": None}),
            "level": user_data.get("level", 1),
            "stats": user_data.get("stats", {"힘": 10, "민첩": 10, "지능": 10}),
            "hp": user_data.get("hp", {"current": 100, "max": 100}),
            "mp": user_data.get("mp", {"current": 50, "max": 50}),
            "exp": user_data.get("exp", 0),
            "exp_to_level": user_data.get("exp_to_level", 100),
            "stat_points": user_data.get("stat_points", 0)
        }



    