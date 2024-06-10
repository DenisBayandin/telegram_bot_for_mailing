from telebot import types

from constants import TEXT_FOR_SAVE_POST, TEXT_FOR_NOT_SAVE_POST


def keyboard_for_post():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_save_post = types.KeyboardButton(text=TEXT_FOR_SAVE_POST)
    key_not_save_post = types.KeyboardButton(text=TEXT_FOR_NOT_SAVE_POST)
    keyboard.add(key_save_post);
    keyboard.add(key_not_save_post)
    return keyboard
