class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def sign_up(self, user_id, password, nickname):
        return self.user_repository.add_user(user_id, password, nickname)

    def authenticate_user(self, user_id, password):
        return self.user_repository.authenticate(user_id, password)

    def get_nickname(self, user_id):
        return self.user_repository.get_nickname(user_id)

    def change_nickname(self, user_id, password, nickname):
        if self.user_repository.authenticate(user_id, password):
            return self.user_repository.change_nickname(user_id, nickname)
        return False

    def delete_user(self, user_id, password):
        if self.user_repository.authenticate(user_id, password):
            return self.user_repository.delete_user(user_id)
        return False
