from telebot import types

from constants import TEXT_FOR_FIRST_ANSWER, TEXT_FOR_SECOND_ANSWER


def keyboard_answer():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_first_answer = types.KeyboardButton(text=TEXT_FOR_FIRST_ANSWER)
    key_second_answer = types.KeyboardButton(text=TEXT_FOR_SECOND_ANSWER)
    keyboard.add(key_first_answer);
    keyboard.add(key_second_answer)
    return keyboard