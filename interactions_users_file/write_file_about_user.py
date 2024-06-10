import json

from datetime import datetime
from functools import lru_cache

from .base import UsersFile


class WriteInformationAbotUser(UsersFile):
    def __init__(self, information_json):
        self.information_json = information_json

    def write_info(self):
        users = self.already_use_data
        with open(self.PATH, "w+") as user_file:
            data_about_user = {self.information_json["id"]: self.information}
            if list(data_about_user.keys())[0] not in list(map(lambda id: int(id), users.keys())):
                json.dump(users | data_about_user, user_file)
            else:
                json.dump(users, user_file)

    @property
    @lru_cache()
    def information(self):
        return {item: self.information_json.get(key) for key, item in self.INFORMATION.items()} | {
            "date_join": datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        }
