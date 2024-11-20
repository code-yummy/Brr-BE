
class PostRepository:
    def __init__(self):
        self.posts = {}
        self.post_counter = 1

    def add_post(self, title, body, user_id):
        post_id = self.post_counter
        self.posts[post_id] = {
            "title": title,
            "body": body,
            "user_id": user_id,
            "written_at": "2024-11-06",
            "modified_at": None,
            "modifier": None,
        }
        self.post_counter += 1
        return post_id

    def get_post(self, post_id):
        return self.posts.get(post_id)

    def update_post(self, post_id, title, body, modifier):
        if post_id in self.posts:
            self.posts[post_id]["title"] = title
            self.posts[post_id]["body"] = body
            self.posts[post_id]["modified_at"] = "2024-11-06"
            self.posts[post_id]["modifier"] = modifier
            return True
        return False

    def delete_post(self, post_id):
        return self.posts.pop(post_id, None) is not None
