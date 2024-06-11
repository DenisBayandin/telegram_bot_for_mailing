from telebot import types

from constants import (TEXT_FOR_BUTTON_CONTENT, TEXT_FOR_BUTTON_EXCLUDE_USERS,
                       TEXT_FOR_BUTTON_USERS, TEXT_FOR_BUTTON_SEND_CONTENT,
                       TEXT_FOR_CURRENT_POST, TEXT_FOR_POSTS)


def keyboard_admin():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_content = types.KeyboardButton(text=TEXT_FOR_BUTTON_CONTENT)
    key_exclude_users = types.KeyboardButton(text=TEXT_FOR_BUTTON_EXCLUDE_USERS)
    key_users = types.KeyboardButton(text=TEXT_FOR_BUTTON_USERS)
    key_send_content = types.KeyboardButton(text=TEXT_FOR_BUTTON_SEND_CONTENT)
    key_show_current_post = types.KeyboardButton(text=TEXT_FOR_CURRENT_POST)
    key_posts = types.KeyboardButton(text=TEXT_FOR_POSTS)
    keyboard.add(key_content);
    keyboard.add(key_show_current_post);
    keyboard.add(key_posts);
    keyboard.add(key_send_content);
    keyboard.add(key_exclude_users);
    keyboard.add(key_users);
    return keyboard
