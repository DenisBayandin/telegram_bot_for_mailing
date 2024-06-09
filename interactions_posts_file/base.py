import json


class PostsFile:
    PATH = "files/posts.json"

    @property
    def already_use_data(self):
        with open(self.PATH, "r") as posts:
            data = posts.read()
            result = json.loads(data) if data else []
        return result
