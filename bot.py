import telebot

from telebot import types

from config import TG_TOKEN, ADMIN_ID
from admin import Admin, EXCLUDE_USERS
from user import User
from constants import *

bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['start'], content_types=['text'])
def send_welcome(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.from_user.id,
                         text="Привет, ты являешься админом, тебе доступен расширенный функционал. Чего ты хочешь?",
                         reply_markup=keyboard_start())
        bot.register_next_step_handler(message, callback_admin)
    else:
        bot.send_message(message.from_user.id, text="Вы добавлены в рассылку!")
        Admin().add_user_in_main_mailing_list(message)


def keyboard_start():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_content = types.KeyboardButton(text=TEXT_FOR_BUTTON_CONTENT)
    key_exclude_users = types.KeyboardButton(text=TEXT_FOR_BUTTON_EXCLUDE_USERS)
    key_users = types.KeyboardButton(text=TEXT_FOR_BUTTON_USERS)
    key_send_content = types.KeyboardButton(text=TEXT_FOR_BUTTON_SEND_CONTENT)
    key_show_current_post = types.KeyboardButton(text=TEXT_FOR_CURRENT_POST)
    key_posts = types.KeyboardButton(text=TEXT_FOR_POSTS)
    keyboard.add(key_content); keyboard.add(key_show_current_post); keyboard.add(key_posts);
    keyboard.add(key_send_content); keyboard.add(key_exclude_users); keyboard.add(key_users);
    return keyboard


@bot.message_handler(content_types=['text'], func=lambda message: message.from_user.id == ADMIN_ID)
def callback_admin(message):
    if message.text == TEXT_FOR_BUTTON_USERS:
        bot.send_message(message.chat.id, Admin.info_about_users())
        bot.register_next_step_handler(message, callback_admin)
    elif message.text == TEXT_FOR_BUTTON_CONTENT:
        bot.send_message(message.from_user.id, text="Что хочешь сохранить?", reply_markup=keyboard_set_content())
        bot.register_next_step_handler(message, content_handler)
    elif message.text == TEXT_FOR_CURRENT_POST:
        callback_current_post(message)
    elif message.text == TEXT_FOR_BUTTON_SEND_CONTENT:
        bot.send_message(message.from_user.id, text="Отправь id поста.")
        bot.register_next_step_handler(message, callback_send_post)
    elif message.text == TEXT_FOR_POSTS:
        callback_posts(message)
    elif message.text == TEXT_FOR_BUTTON_EXCLUDE_USERS:
        bot.send_message(message.from_user.id, text="Чего хочешь?", reply_markup=keyboard_exclude_users())
        bot.register_next_step_handler(message, callback_exclude_user)


@bot.message_handler(content_types=['text'], func=lambda message: message.from_user.id == ADMIN_ID)
def callback_exclude_user(message):
    if message.text == TEXT_FOR_SHOW_EXCLUDE_USERS:
        bot.send_message(message.from_user.id, text=Admin().show_exclude_users(), reply_markup=keyboard_start())
        bot.register_next_step_handler(message, callback_admin)
    if message.text == TEXT_FOR_EXCLUDE_USER:
        bot.send_message(message.from_user.id, text="Укажите ID пользователя.", reply_markup=None)
        bot.register_next_step_handler(message, callback_add_user_in_exclude)
    if message.text == TEXT_FOR_REMOVE_EXCLUDE_USER:
        bot.send_message(message.from_user.id, text="Укажите ID пользователя.", reply_markup=None)
        bot.register_next_step_handler(message, callback_remove_user_in_exclude)


@bot.message_handler(content_types=['text'], func=lambda message: message.from_user.id == ADMIN_ID)
def callback_add_user_in_exclude(message):
    bot.send_message(message.from_user.id, Admin().add_exclude_user(message.text), reply_markup=keyboard_start())
    bot.register_next_step_handler(message, callback_admin)


@bot.message_handler(content_types=['text'], func=lambda message: message.from_user.id == ADMIN_ID)
def callback_remove_user_in_exclude(message):
    bot.send_message(message.from_user.id, Admin().remove_exclude_user(message.text), reply_markup=keyboard_start())
    bot.register_next_step_handler(message, callback_admin)


def keyboard_exclude_users():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_exclude_user = types.KeyboardButton(text=TEXT_FOR_EXCLUDE_USER)
    key_remove_exclude_user = types.KeyboardButton(text=TEXT_FOR_REMOVE_EXCLUDE_USER)
    key_show_exclude_users = types.KeyboardButton(text=TEXT_FOR_SHOW_EXCLUDE_USERS)
    keyboard.add(key_show_exclude_users); keyboard.add(key_exclude_user); keyboard.add(key_remove_exclude_user)
    return keyboard


def keyboard_set_content():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_content_photo = types.KeyboardButton(text=TEXT_FOR_BUTTON_CONTENT_PHOTO)
    key_content_text = types.KeyboardButton(text=TEXT_FOR_BUTTON_CONTENT_TEXT)
    keyboard.add(key_content_text); keyboard.add(key_content_photo)
    return keyboard


@bot.message_handler(content_types=['text'], func=lambda message: message.from_user.id == ADMIN_ID)
def content_handler(message):
    if message.content_type == "photo" or message.text == TEXT_FOR_BUTTON_CONTENT_PHOTO:
        bot.send_message(message.from_user.id, text="Отправь фотографию!", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, callback_set_content_photo)
    elif message.text == TEXT_FOR_BUTTON_CONTENT_TEXT:
        bot.send_message(message.from_user.id, text="Отправь текст!", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, callback_set_content_text)


@bot.message_handler(content_types=['photo'], func=lambda message: message.from_user.id == ADMIN_ID)
def callback_set_content_photo(message):
    Admin().set_photo(message, bot, TG_TOKEN)
    bot.send_message(message.from_user.id, "Успешно сохранено! Вернемся назад.", reply_markup=keyboard_start())
    bot.register_next_step_handler(message, callback_admin)


@bot.message_handler(content_types=['text'], func=lambda message: message.from_user.id == ADMIN_ID)
def callback_set_content_text(message):
    Admin().set_content(message)
    bot.send_message(message.from_user.id, "Успешно сохранено! Вернемся назад.", reply_markup=keyboard_start())
    bot.register_next_step_handler(message, callback_admin)


def callback_current_post(message):
    photo, content = Admin().show_current_post()
    if photo:
        bot.send_photo(message.from_user.id, photo=open(photo, "rb"), caption=content, reply_markup=keyboard_for_post())
    elif content:
        bot.send_message(message.from_user.id, content)
    else:
        bot.send_message(message.from_user.id, "Нет данных")
    bot.register_next_step_handler(message, post_handler)


@bot.message_handler(content_types=['text'], func=lambda message: message.from_user.id == ADMIN_ID)
def post_handler(message):
    if message.text == TEXT_FOR_SAVE_POST:
        Admin().create_post()
        bot.send_message(message.from_user.id, "Успешно сохранено! Вернемся назад.", reply_markup=keyboard_start())
        bot.register_next_step_handler(message, send_welcome)
    elif message.text == TEXT_FOR_NOT_SAVE_POST:
        bot.send_message(message.from_user.id, "Вернёмся к редактированию поста!", reply_markup=keyboard_set_content())
        bot.register_next_step_handler(message, content_handler)


def keyboard_for_post():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_save_post = types.KeyboardButton(text=TEXT_FOR_SAVE_POST)
    key_not_save_post = types.KeyboardButton(text=TEXT_FOR_NOT_SAVE_POST)
    keyboard.add(key_save_post); keyboard.add(key_not_save_post)
    return keyboard


@bot.message_handler(content_types=['text'])
def callback_send_post(message):
    post_id = int(message.text)
    post = Admin().search_post(post_id)
    if post:
        photo, content = post.get("photo"), post.get("content")
        users_id = list(filter(lambda user_id: user_id not in EXCLUDE_USERS, Admin().show_users_which_send_post()))
        message_user = None
        for id in users_id:
            if photo:
                message_user = bot.send_photo(id, photo=open(photo, "rb"), caption=content,
                               reply_markup=keyboard_answer())
            elif content:
                message_user = bot.send_message(id, content, reply_markup=keyboard_answer())
        if message_user:
            bot.send_message(message.from_user.id, text="Все пользователи успешно получили сообщение!")
            bot.register_next_step_handler(message_user, callback_answer, {"post": post})
        else:
            bot.send_message(message.from_user.id, text="Нет пользователей, которые могли бы получить рассылку!")


def keyboard_answer():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_first_answer = types.KeyboardButton(text=TEXT_FOR_FIRST_ANSWER)
    keyboard.add(key_first_answer)
    return keyboard


@bot.message_handler(content_types=['text'])
def callback_answer(message, post):
    User().set_answer(message, post['post'])


def callback_posts(message):
    posts = Admin().posts()
    if not posts:
        return bot.send_message(message.from_user.id, text="Публикаций нет!")
    for post in posts:
        bot.send_photo(message.from_user.id, photo=open(post.get('photo'), "rb"), caption=f"ID поста: {post.get('id')}\n"
                                                                                          f"{post.get('content')}\n"
                                                                                          f"Ответы: \n{str_answer(post['answer']) if post.get('answer') else 'Нет ответов.'}\n"
                                                                                          f"Дата создания: {post.get('date_create')}")


def str_answer(answers):
    return "".join([f"Ник пользователя: {answer['username']}\n"
                    f"ID пользователя: {answer['user_id']}\n"
                    f"Ответ: {answer['text']}\n" for answer in answers])


bot.polling(none_stop=True, interval=0)
