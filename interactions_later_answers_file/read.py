
from .base import LaterAnswerFile


class ReadLaterAnswerFile(LaterAnswerFile):
    @property
    def check_current_date_exists(self):
        return (True if self.TODAY in self.already_use_data.keys() else False) if self.already_use_data else None

    @property
    def show_later_answers(self):
        return self.already_use_data[self.TODAY]
