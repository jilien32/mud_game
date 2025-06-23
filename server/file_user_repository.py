import json
import os
from .user_repository import UserRepository

class FileUserRepository(UserRepository):
    def __init__(self, path='users.json'):
        self.path = path

    def load_users(self):
        if not os.path.exists(self.path):
            return {}
        with open(self.path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_users(self, users: dict):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
