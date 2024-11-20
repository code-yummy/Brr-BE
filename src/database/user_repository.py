class UserRepository:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, password, nickname):
        if user_id in self.users:
            return False
        self.users[user_id] = {"password": password, "nickname": nickname}
        return True

    def authenticate(self, user_id, password):
        user = self.users.get(user_id)
        return user and user["password"] == password

    def get_nickname(self, user_id):
        user = self.users.get(user_id)
        return user["nickname"] if user else None

    def change_nickname(self, user_id, nickname):
        if user_id in self.users:
            self.users[user_id]["nickname"] = nickname
            return True
        return False

    def delete_user(self, user_id):
        return self.users.pop(user_id, None) is not None
