class World:
    def __init__(self):
        self.rooms = {
            'start': {
                'description': '당신은 시작 방에 있습니다. 동쪽으로 갈 수 있습니다.',
                'exits': {'동': 'hall'}
            },
            'hall': {
                'description': '넓은 복도입니다. 서쪽으로 갈 수 있습니다.',
                'exits': {'서': 'start'}
            }
        }

    def get_room(self, room_id):
        return self.rooms.get(room_id, {})
