import telebot
import time

from telebot import types
from threading import Thread

from config import TG_TOKEN, ADMIN_ID
from admin import Admin, EXCLUDE_USERS
from user import User
from constants import *
from interactions_later_answers_file.read import ReadLaterAnswerFile
from interactions_later_answers_file.write import WriteLaterAnswerFile
from keyboards.answer import keyboard_answer
from keyboards.exclude_user import keyboard_exclude_users
from keyboards.post import keyboard_for_post
from keyboards.set_content import keyboard_set_content
from keyboards.admin import keyboard_admin
from keyboards.posts import keyboard_posts
from utils import str_answer


bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['admin'], content_types=['text'], func=lambda message: message.from_user.id in ADMIN_ID)
def start_admin(message):
    bot.send_message(message.from_user.id,
                     text="Привет, ты являешься админом, тебе доступен расширенный функционал. Чего ты хочешь?",
                     reply_markup=keyboard_admin())
    bot.register_next_step_handler(message, admin_handler)


@bot.message_handler(content_types=['text'], func=lambda message: message.from_user.id not in ADMIN_ID)
def start_another_user(message):
    bot.send_message(message.from_user.id, text="Вы добавлены в рассылку!")
    Admin().add_user_in_main_mailing_list(message)


@bot.message_handler(content_types=['text'], func=lambda message: message.from_user.id in ADMIN_ID)
def admin_handler(message):
    if message.text == TEXT_FOR_BUTTON_USERS:
        bot.send_message(message.chat.id, Admin.info_about_users())
        bot.register_next_step_handler(message, admin_handler)
    elif message.text == TEXT_FOR_BUTTON_CONTENT:
        bot.send_message(message.from_user.id,
                         text="Что хочешь сохранить? "
                         "Учти, что вместе с фотографией можно отправить только 1000 символов.",
                         reply_markup=keyboard_set_content())
        bot.register_next_step_handler(message, content_handler)
    elif message.text == TEXT_FOR_CURRENT_POST:
        callback_current_post(message)
    elif message.text == TEXT_FOR_BUTTON_SEND_CONTENT:
        bot.send_message(message.from_user.id, text="Отправь id поста.", reply_markup=keyboard_posts())
        bot.register_next_step_handler(message, callback_send_post)
    elif message.text == TEXT_FOR_POSTS:
        callback_posts(message)
    elif message.text == TEXT_FOR_BUTTON_EXCLUDE_USERS:
        bot.send_message(message.from_user.id, text="Чего хочешь?", reply_markup=keyboard_exclude_users())
        bot.register_next_step_handler(message, exclude_user_handler)


@bot.message_handler(content_types=['text'], func=lambda message: message.from_user.id in ADMIN_ID)
def exclude_user_handler(message):
    if message.text == TEXT_FOR_SHOW_EXCLUDE_USERS:
        bot.send_message(message.from_user.id, text=Admin().show_exclude_users(), reply_markup=keyboard_admin())
        bot.register_next_step_handler(message, admin_handler)
    elif message.text == TEXT_FOR_EXCLUDE_USER:
        bot.send_message(message.from_user.id, text="Укажите ID пользователя.", reply_markup=None)
        bot.register_next_step_handler(message, callback_add_user_in_exclude)
    elif message.text == TEXT_FOR_REMOVE_EXCLUDE_USER:
        bot.send_message(message.from_user.id, text="Укажите ID пользователя.", reply_markup=None)
        bot.register_next_step_handler(message, callback_remove_user_in_exclude)
    elif message.text == TEXT_FOR_RETURN_TO_BACK:
        bot.send_message(message.from_user.id, text="Вернёмся назад!", reply_markup=keyboard_admin())


@bot.message_handler(content_types=['text'], func=lambda message: message.from_user.id in ADMIN_ID)
def callback_add_user_in_exclude(message):
    bot.send_message(message.from_user.id, Admin().add_exclude_user(message.text), reply_markup=keyboard_admin())
    bot.register_next_step_handler(message, admin_handler)


@bot.message_handler(content_types=['text'], func=lambda message: message.from_user.id in ADMIN_ID)
def callback_remove_user_in_exclude(message):
    bot.send_message(message.from_user.id, Admin().remove_exclude_user(message.text), reply_markup=keyboard_admin())
    bot.register_next_step_handler(message, admin_handler)


@bot.message_handler(content_types=['text'], func=lambda message: message.from_user.id in ADMIN_ID)
def content_handler(message):
    if message.content_type == "photo" or message.text == TEXT_FOR_BUTTON_CONTENT_PHOTO:
        bot.send_message(message.from_user.id, text="Отправь фотографию!", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, callback_set_content_photo)
    elif message.text == TEXT_FOR_BUTTON_CONTENT_TEXT:
        bot.send_message(message.from_user.id, text="Отправь текст!", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, callback_set_content_text)
    elif message.text == TEXT_FOR_RETURN_TO_BACK:
        bot.send_message(message.from_user.id, text="Вернёмся назад!", reply_markup=keyboard_admin())


@bot.message_handler(content_types=['photo'], func=lambda message: message.from_user.id in ADMIN_ID)
def callback_set_content_photo(message):
    Admin().set_photo(message, bot, TG_TOKEN)
    bot.send_message(message.from_user.id, "Успешно сохранено! Вернемся назад.", reply_markup=keyboard_admin())
    bot.register_next_step_handler(message, admin_handler)


@bot.message_handler(content_types=['text'], func=lambda message: message.from_user.id in ADMIN_ID)
def callback_set_content_text(message):
    Admin().set_content(message)
    bot.send_message(message.from_user.id, "Успешно сохранено! Вернемся назад.", reply_markup=keyboard_admin())
    bot.register_next_step_handler(message, admin_handler)


def callback_current_post(message):
    photo, content = Admin().show_current_post()
    if photo:
        bot.send_photo(message.from_user.id, photo=open(photo, "rb"), caption=content, reply_markup=keyboard_for_post())
    elif content:
        bot.send_message(message.from_user.id, content, reply_markup=keyboard_for_post())
    else:
        bot.send_message(message.from_user.id, "Нет данных")
    bot.register_next_step_handler(message, post_handler)


@bot.message_handler(content_types=['text'], func=lambda message: message.from_user.id in ADMIN_ID)
def post_handler(message):
    if message.text == TEXT_FOR_SAVE_POST:
        Admin().create_post()
        bot.send_message(message.from_user.id, "Успешно сохранено! Вернемся назад!", reply_markup=keyboard_admin())
        bot.register_next_step_handler(message, admin_handler)
    elif message.text == TEXT_FOR_NOT_SAVE_POST:
        bot.send_message(message.from_user.id, "Вернёмся к редактированию поста!", reply_markup=keyboard_set_content())
        bot.register_next_step_handler(message, content_handler)
    elif message.text == TEXT_FOR_RETURN_TO_BACK:
        bot.send_message(message.from_user.id, "Вернёмся назад!", reply_markup=keyboard_admin())


@bot.message_handler(content_types=['text'])
def callback_send_post(message):
    post_id = int(message.text)
    post = Admin().search_post(post_id)
    if post:
        photo, content = post.get("photo"), post.get("content")
        users_id = list(filter(lambda user_id: user_id not in EXCLUDE_USERS, Admin().show_users_which_send_post()))
        message_user = None
        for user_id in users_id:
            if post.get('photo') and post.get('content'):
                message_user = bot.send_photo(user_id, photo=open(photo, "rb"), caption=content,
                                              reply_markup=keyboard_answer())
            elif post.get("photo"):
                message_user = bot.send_photo(user_id, photo=open(photo, "rb"), reply_markup=keyboard_answer())
            elif post.get("content"):
                message_user = bot.send_message(user_id, text=content, reply_markup=keyboard_answer())
        if message_user:
            bot.send_message(message.from_user.id,
                             text="Все пользователи успешно получили сообщение!",
                             reply_markup=keyboard_admin())
            bot.register_next_step_handler(message_user, callback_answer, {"post": post})
        else:
            bot.send_message(message.from_user.id,
                             text="Нет пользователей, которые могли бы получить рассылку!",
                             reply_markup=keyboard_admin())


@bot.message_handler(content_types=['text'])
def callback_answer(message, post):
    correct_answer = True
    if message.text == TEXT_FOR_FIRST_ANSWER:
        User().set_answer_later(days=3, post=post['post'], user_id=message.from_user.id)
        correct_answer = False
    if message.text == TEXT_FOR_SECOND_ANSWER:
        User().set_answer_later(days=7, post=post['post'], user_id=message.from_user.id)
        correct_answer = False
    User().set_answer(message, post['post'])
    if correct_answer:
        bot.send_message(message.from_user.id,
                         "Спасибо за ответ!",
                         reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.from_user.id,
                         "Спасибо, мы напишем позже!",
                         reply_markup=types.ReplyKeyboardRemove())


def callback_posts(message):
    posts = Admin().posts()
    if not posts:
        return bot.send_message(message.from_user.id, text="Публикаций нет!")
    for post in sorted(posts, key=lambda post_sort: post_sort['id']):
        if post.get('photo') and post.get('content'):
            bot.send_photo(message.from_user.id, photo=open(post.get('photo'), "rb"),
                           caption=f"ID поста: {post.get('id')}\n"
                                   f"{post.get('content')}\n"
                                   f"Ответы: \n{str_answer(post['answer']) if post.get('answer') else 'Нет ответов.'}\n"
                                   f"Дата создания: {post.get('date_create')}")
        elif post.get('photo'):
            bot.send_photo(message.from_user.id, photo=open(post.get('photo'), "rb"),
                           caption=f"ID поста: {post.get('id')}\n"
                                   f"Ответы: \n{str_answer(post['answer']) if post.get('answer') else 'Нет ответов.'}\n"
                                   f"Дата создания: {post.get('date_create')}")
        elif post.get('content'):
            bot.send_message(message.from_user.id,
                             text=f"ID поста: {post.get('id')}\n"
                                   f"{post.get('content')}\n"
                                   f"Ответы: \n{str_answer(post['answer']) if post.get('answer') else 'Нет ответов.'}\n"
                                   f"Дата создания: {post.get('date_create')}")


@bot.message_handler(content_types=['text'])
def callback_later_answer():
    while True:
        if ReadLaterAnswerFile().check_current_date_exists:
            for later_answer in ReadLaterAnswerFile().show_later_answers:
                message_user = bot.send_message(later_answer['user_id'],
                                                "Привет, ты обещал дать ответ!",
                                                reply_markup=keyboard_answer())
                bot.register_next_step_handler(message_user, callback_answer, {"post": later_answer['post']})
            WriteLaterAnswerFile().remove_today_answer()
        time.sleep(10800)


Thread(target=callback_later_answer).start()
bot.polling(none_stop=True, interval=0)
