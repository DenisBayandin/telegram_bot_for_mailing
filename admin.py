import requests

from interactions_users_file.write_file_about_user import WriteInformationAbotUser
from interactions_users_file.read_file_about_user import ReadInformationAbotUser
from interactions_posts_file.write_file_about_post import WritePost
from interactions_posts_file.read_file_about_post import ReadPost

CURRENT_PHOTO = ""
CURRENT_CONTENT = ""
EXCLUDE_USERS = []


class Admin:
    def add_user_in_main_mailing_list(self, message):
        return WriteInformationAbotUser(message.from_user.to_dict()).write_info()

    @classmethod
    def info_about_users(cls):
        result = ReadInformationAbotUser().show_users()
        return result if result else "Ещё нет таких людей!"

    def set_photo(self, message, bot, token):
        global CURRENT_PHOTO
        file_id = message.photo[-1].file_id
        file_path = bot.get_file(file_id).file_path
        photo_url = 'https://api.telegram.org/file/bot{}/{}'.format(token, file_path)
        response = requests.get(photo_url)
        path = 'uploads/{}.jpg'.format(file_id)
        CURRENT_PHOTO = path
        with open(path, 'wb+') as file:
            file.write(response.content)

    def set_content(self, message):
        global CURRENT_CONTENT
        CURRENT_CONTENT = message.text

    def show_current_post(self):
        return CURRENT_PHOTO, CURRENT_CONTENT

    def show_users_which_send_post(self):
        return ReadInformationAbotUser().show_users_id()

    def create_post(self):
        WritePost(content=CURRENT_CONTENT, photo=CURRENT_PHOTO).write_post()

    def posts(self):
        return ReadPost().show_posts()

    def search_post(self, post_id):
        for post in ReadPost().show_posts():
            if post["id"] == post_id:
                return post
        return None

    def add_exclude_user(self, user_id):
        if user_id in EXCLUDE_USERS:
            return "Пользователь и так в списке исключенных!"
        else:
            users_id = ReadInformationAbotUser().show_users_id()
            if user_id in users_id:
                EXCLUDE_USERS.append(user_id)
                return f"Список id-ников исключенных из рассылки: " + "".join(EXCLUDE_USERS)
            return "Пользователя с таким ID не существует!"

    def remove_exclude_user(self, user_id):
        if not EXCLUDE_USERS:
            return "Список пуст, поэтому удаление невозможно!"
        elif user_id not in EXCLUDE_USERS:
            return "Пользователя нет в списке исключенных!"
        else:
            users_id = ReadInformationAbotUser().show_users_id()
            if user_id in users_id:
                EXCLUDE_USERS.remove(user_id)
                return f"Список id-ников исключенных из рассылки: " + "".join(EXCLUDE_USERS)
            return "Пользователя с таким ID не существует!"

    def show_exclude_users(self):
        return f"Список id-ников исключенных из рассылки: " + "".join(EXCLUDE_USERS) if\
            EXCLUDE_USERS else "Пользователей не найдено!"
