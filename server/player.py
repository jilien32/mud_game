class Player:
    def __init__(self, name, location='start', inventory=None, equipment=None,
                 level=1, stats=None, hp=None, mp=None,
                 exp=0, exp_to_level=100, stat_points=0):
        self.name = name
        self.location = location
        self.inventory = inventory if inventory else []
        self.equipment = equipment if equipment else {"무기": None, "방어구": None}
        self.level = level
        self.stats = stats if stats else {"힘": 10, "민첩": 10, "지능": 10}
        self.hp = hp if hp else {"current": 100, "max": 100}
        self.mp = mp if mp else {"current": 50, "max": 50}
        self.exp = exp
        self.exp_to_level = exp_to_level
        self.stat_points = stat_points

    def to_dict(self):
        return {
            "location": self.location,
            "inventory": self.inventory,
            "equipment": self.equipment,
            "level": self.level,
            "stats": self.stats,
            "hp": self.hp,
            "mp": self.mp,
            "exp": self.exp,
            "exp_to_level": self.exp_to_level,
            "stat_points": self.stat_points
        }

    def load_data(self, data):
        self.location = data.get("location", "start")
        self.inventory = data.get("inventory", [])
        self.equipment = data.get("equipment", {"무기": None, "방어구": None})
        self.level = data.get("level", 1)
        self.stats = data.get("stats", {"힘": 10, "민첩": 10, "지능": 10})
        self.hp = data.get("hp", {"current": 100, "max": 100})
        self.mp = data.get("mp", {"current": 50, "max": 50})
        self.exp = data.get("exp", 0)
        self.exp_to_level = data.get("exp_to_level", 100)
        self.stat_points = data.get("stat_points", 0)
