from server.player import Player

class UserManager:
    def __init__(self, repository):
        self.repository = repository
        self.users = self.repository.load_users()

    def register(self, user_id, password):
        if user_id in self.users:
            return False, "이미 존재하는 아이디입니다."
        self.users[user_id] = {
            'password': password,
            'level': 1,
            'hp': 100,
            'mp': 50,
            'str_': 5,
            'dex': 5,
            'int_': 5,
            'x': 0, 'y': 0, 'z': 0,
            'inventory': [],
            'equipped': {"무기": None, "방어구": None},
            'kingdom': '중립',
            'exp': 0,
            'stat_points': 0
        }
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
        x, y, z = user_data.get("x", 0), user_data.get("y", 0), user_data.get("z", 0)

        return {
            "x": x,
            "y": y,
            "z": z,
            "inventory": user_data.get("inventory", []),
            "equipped": user_data.get("equipped", {"무기": None, "방어구": None}),
            "level": user_data.get("level", 1),
            "str_": user_data.get("str_", 5),
            "dex": user_data.get("dex", 5),
            "int_": user_data.get("int_", 5),
            "hp": user_data.get("hp", 100),
            "mp": user_data.get("mp", 50),
            "exp": user_data.get("exp", 0),
            "stat_points": user_data.get("stat_points", 0),
            "kingdom": user_data.get("kingdom", "중립")
        }




    