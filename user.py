from interactions_posts_file.write_file_about_post import WritePost


class User:
    def set_answer(self, message, post):
        post["answer"].append({"text": message.text,
                               "username": message.from_user.username,
                               "user_id": message.from_user.id})
        WritePost().write_answer(post)
