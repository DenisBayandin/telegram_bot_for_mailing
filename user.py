from interactions_posts_file.write_file_about_post import WritePost
from interactions_later_answers_file.write import WriteLaterAnswerFile


class User:
    def set_answer(self, message, post):
        post["answer"].append({"text": message.text,
                               "username": message.from_user.username,
                               "user_id": message.from_user.id})
        WritePost().write_answer(post)

    def set_answer_later(self, days, post, user_id):
        WriteLaterAnswerFile(days, post, user_id).write_later_answer()
