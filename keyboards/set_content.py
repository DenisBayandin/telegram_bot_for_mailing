from telebot import types

from constants import TEXT_FOR_BUTTON_CONTENT_PHOTO, TEXT_FOR_BUTTON_CONTENT_TEXT, TEXT_FOR_RETURN_TO_BACK


def keyboard_set_content():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_content_photo = types.KeyboardButton(text=TEXT_FOR_BUTTON_CONTENT_PHOTO)
    key_content_text = types.KeyboardButton(text=TEXT_FOR_BUTTON_CONTENT_TEXT)
    key_return_back = types.KeyboardButton(text=TEXT_FOR_RETURN_TO_BACK)
    keyboard.add(key_content_text);
    keyboard.add(key_content_photo);
    keyboard.add(key_return_back)
    return keyboard
