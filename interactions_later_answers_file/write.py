import json

from datetime import date, timedelta

from .base import LaterAnswerFile


class WriteLaterAnswerFile(LaterAnswerFile):
    def __init__(self, after_days=None, post=None, user_id=None):
        self.after_days = after_days
        self.post = post
        self.user_id = user_id

    def write_later_answer(self):
        answers = self.already_use_data
        custom_date = (date.today() + timedelta(days=self.after_days)).strftime("%Y.%m.%d")
        if answers.get(custom_date):
            if self.later_answer not in answers[custom_date]:
                answers[custom_date].append(self.later_answer)
        else:
            answers[custom_date] = [self.later_answer]
        with open(self.PATH, "w+") as later_answers_file:
            json.dump(answers, later_answers_file)

    @property
    def later_answer(self):
        return {"post": self.post, "user_id": self.user_id}

    def remove_today_answer(self):
        answers = self.already_use_data
        answers.pop(self.TODAY, None)
        with open(self.PATH, "w+") as later_answers_file:
            json.dump(answers, later_answers_file)
