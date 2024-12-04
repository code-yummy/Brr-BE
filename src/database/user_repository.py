class UserRepository:
    def __init__(self):
        self.users = {}

    def add_user(self, email, password, nickname):
        if email in self.users:
            return False
        self.users[email] = {"password": password, "nickname": nickname}
        return True

    def authenticate(self, email, password):
        user = self.users.get(email)
        return user and user["password"] == password

    def get_nickname(self, email):
        user = self.users.get(email)
        return user["nickname"] if user else None

    def change_nickname(self, email, nickname):
        if email in self.users:
            self.users[email]["nickname"] = nickname
            return True
        return False

    def delete_user(self, email):
        return self.users.pop(email, None) is not None
