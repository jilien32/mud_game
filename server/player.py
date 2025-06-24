class Player:
    def __init__(
        self,
        user_id: str,
        level: int = 1,
        hp: int = 100,
        mp: int = 50,
        str_: int = 5,
        dex: int = 5,
        int_: int = 5,
        x: int = 0,
        y: int = 0,
        z: int = 0,
        inventory: list = None,
        equipped: dict = None,
        kingdom: str = "중립",
        exp: int = 0,
        stat_points: int = 0,
        conn=None
    ):
        self.user_id = user_id
        self.level = level
        self.hp = hp
        self.mp = mp
        self.str = str_
        self.dex = dex
        self.int = int_
        self.x = x
        self.y = y
        self.z = z
        self.inventory = inventory if inventory else []
        self.equipped = equipped if equipped else {}
        self.kingdom = kingdom
        self.exp = exp
        self.stat_points = stat_points
        self.conn = conn

    @property
    def get_location(self):
        return (self.x, self.y, self.z)

    def set_location(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def to_dict(self):
        return {
            "level": self.level,
            "hp": self.hp,
            "mp": self.mp,
            "str_": self.str,
            "dex": self.dex,
            "int_": self.int,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "inventory": self.inventory,
            "equipped": self.equipped,
            "kingdom": self.kingdom,
            "exp": self.exp,
            "stat_points": self.stat_points
        }

    @staticmethod
    def load_data(user_id: str, data: dict):
        """딕셔너리에서 Player 객체 생성"""
        return Player(
            user_id=user_id,
            level=data.get("level", 1),
            hp=data.get("hp", 100),
            mp=data.get("mp", 50),
            str_=data.get("str_", 5),
            dex=data.get("dex", 5),
            int_=data.get("int_", 5),
            x=data.get("x", 0),
            y=data.get("y", 0),
            z=data.get("z", 0),
            inventory=data.get("inventory", []),
            equipped=data.get("equipped", {}),
            kingdom=data.get("kingdom", "중립"),
            exp=data.get("exp", 0),
            stat_points=data.get("stat_points", 0)
        )

    def apply_stat_effects(self):
        self.hp = 100 + self.str * 10
        self.mp = 50 + self.int * 10

    def add_exp(self, amount: int):
        self.exp += amount
        while self.exp >= 100:
            self.exp -= 100
            self.level += 1
            self.stat_points += 3
