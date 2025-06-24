from abc import ABC, abstractmethod
import json
import os

class FileUserRepository:
    def __init__(self, filepath="users.json"):
        self.filepath = filepath

    def load_users(self):
        if not os.path.exists(self.filepath):
            return {}
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_users(self, users):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

class UserRepository(ABC):
    @abstractmethod
    def load_users(self):
        pass

    @abstractmethod
    def save_users(self, users: dict):
        pass
