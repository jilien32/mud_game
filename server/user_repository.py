from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def load_users(self):
        pass

    @abstractmethod
    def save_users(self, users: dict):
        pass
