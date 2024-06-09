import json


class UsersFile:
    PATH = "files/users.json"
    INFORMATION = {
        "first_name": "first_name",
        "last_name": "last_name",
        "username": "username",
        "is_premium": "is_premium"
    }

    @property
    def already_use_data(self):
        with open(self.PATH, "r") as users:
            data = users.read()
            return json.loads(data) if data else {}
