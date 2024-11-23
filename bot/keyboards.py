from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard(authenticated=False):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if authenticated:
        keyboard.add(KeyboardButton("Выйти"))
    else:
        keyboard.add(KeyboardButton("Войти"))
    return keyboard
