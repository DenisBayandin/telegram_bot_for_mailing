from telebot import types

from constants import TEXT_FOR_SAVE_POST, TEXT_FOR_NOT_SAVE_POST, TEXT_FOR_RETURN_TO_BACK


def keyboard_for_post():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_save_post = types.KeyboardButton(text=TEXT_FOR_SAVE_POST)
    key_not_save_post = types.KeyboardButton(text=TEXT_FOR_NOT_SAVE_POST)
    key_return_back = types.KeyboardButton(text=TEXT_FOR_RETURN_TO_BACK)
    keyboard.add(key_save_post);
    keyboard.add(key_not_save_post);
    keyboard.add(key_return_back)
    return keyboard
