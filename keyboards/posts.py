from telebot import types
from interactions_posts_file.read_file_about_post import ReadPost


def keyboard_posts():
    keyboard = types.ReplyKeyboardMarkup()
    posts_id = sorted([post['id'] for post in ReadPost().already_use_data])
    for post_id in posts_id:
        keyboard.add(types.InlineKeyboardButton(post_id, callback_data=post_id))
    return keyboard
