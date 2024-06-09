from .base import PostsFile


class ReadPost(PostsFile):
    def show_posts(self):
        return self.already_use_data

