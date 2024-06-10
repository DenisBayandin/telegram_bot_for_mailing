from telebot import types

from constants import TEXT_FOR_EXCLUDE_USER, TEXT_FOR_REMOVE_EXCLUDE_USER, TEXT_FOR_SHOW_EXCLUDE_USERS


def keyboard_exclude_users():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_exclude_user = types.KeyboardButton(text=TEXT_FOR_EXCLUDE_USER)
    key_remove_exclude_user = types.KeyboardButton(text=TEXT_FOR_REMOVE_EXCLUDE_USER)
    key_show_exclude_users = types.KeyboardButton(text=TEXT_FOR_SHOW_EXCLUDE_USERS)
    keyboard.add(key_show_exclude_users);
    keyboard.add(key_exclude_user);
    keyboard.add(key_remove_exclude_user)
    return keyboard
