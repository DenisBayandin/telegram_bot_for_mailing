import json

from datetime import date, timedelta


class LaterAnswerFile:
    PATH = "files/later_answers.json"
    TODAY = date.today().strftime("%Y.%m.%d")

    @property
    def already_use_data(self):
        with open(self.PATH, "r") as posts:
            data = posts.read()
            result = json.loads(data) if data else {}
        return result
