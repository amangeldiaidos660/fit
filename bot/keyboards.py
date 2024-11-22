from telebot.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(KeyboardButton("Войти"), KeyboardButton("Записать тренировку"))
main_keyboard.add(KeyboardButton("Мой прогресс"))
