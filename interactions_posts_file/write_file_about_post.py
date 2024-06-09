import json

from datetime import datetime
from functools import lru_cache

from .base import PostsFile


class WritePost(PostsFile):
    def __init__(self, photo="", content=""):
        self.photo = photo
        self.content = content

    def write_post(self):
        posts = self.already_use_data
        current_post_id = max([int(i["id"]) for i in posts]) + 1 if posts else 1
        with open(self.PATH, "+w") as post_file:
            posts.append(self.post(current_post_id))
            json.dump(posts, post_file)

    def write_answer(self, post_with_answer):
        posts = self.already_use_data
        for post in posts:
            if post['id'] == post_with_answer['id']:
                posts.remove(post)
                posts.append(post_with_answer)
        with open(self.PATH, "+w") as post_file:
            json.dump(posts, post_file)

    @lru_cache()
    def post(self, post_id):
        return {"id": post_id,
                "content": self.content,
                "photo": self.photo,
                "date_create": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                "answer": []}
