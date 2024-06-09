from .base import UsersFile


class ReadInformationAbotUser(UsersFile):
    READ_INFORMATION = {
        "id": "ID",
        "first_name": "Имя",
        "last_name": "Фамилия",
        "username": "Ник",
        "is_premium": "Премиум аккаунт?",
        "date_join": "Дата и время подписки"
    }

    def show_users(self):
        result = []
        for key, item in self.already_use_data.items():
            result.append(f"ID пользователя - {key}")
            result.append("\n".join(f"{self.READ_INFORMATION.get(key)} - {item}" for key, item in item.items()))
        return "\n\n".join(result)

    def show_users_id(self):
        return [id for id in self.already_use_data.keys()]

