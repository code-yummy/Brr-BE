class PostService:
    def __init__(self, post_repository):
        self.post_repository = post_repository

    def create_post(self, title, body, user_id):
        return self.post_repository.add_post(title, body, user_id)

    def read_post(self, post_id):
        return self.post_repository.get_post(post_id)

    def update_post(self, post_id, title, body, user_id):
        post = self.post_repository.get_post(post_id)
        if post and post["user_id"] == user_id:
            return self.post_repository.update_post(post_id, title, body, user_id)
        return False

    def delete_post(self, post_id, user_id):
        post = self.post_repository.get_post(post_id)
        if post and post["user_id"] == user_id:
            return self.post_repository.delete_post(post_id)
        return False
