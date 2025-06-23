class Player:
    def __init__(self, name, location='start'):
        self.name = name
        self.location = location

    def move(self, direction, world):
        room = world.get_room(self.location)
        if direction in room['exits']:
            self.location = room['exits'][direction]
            return f"{self.name}님이 {direction} 방향으로 이동했습니다."
        else:
            return "그 방향으로는 갈 수 없습니다."
