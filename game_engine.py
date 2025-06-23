from .player import Player
from .world import World

class GameEngine:
    def __init__(self):
        self.world = World()
        self.players = {}

    def add_player(self, name):
        self.players[name] = Player(name)
        return f"{name}님이 게임에 입장했습니다."

    def process_command(self, name, command):
        player = self.players.get(name)
        if not player:
            return "플레이어가 없습니다."

        if command.startswith("이동 "):
            direction = command.split(" ", 1)[1]
            return player.move(direction, self.world)
        elif command == "주변":
            room = self.world.get_room(player.location)
            return room.get('description', '아무것도 없습니다.')
        else:
            return "알 수 없는 명령어입니다."
