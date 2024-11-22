from telebot.types import Message
from keyboards import main_keyboard
from progress import show_progress_menu
from auth import auth_bot

def start(bot, message: Message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Выберите команду из меню или отправьте голосовое сообщение.",
        reply_markup=main_keyboard,
    )

def handle_menu_command(bot, message: Message):
    if message.text == "Войти":
        bot.reply_to(message, "Вы вошли в систему. Что вы хотите сделать дальше?")
        auth_bot(bot, message.chat.id)
    elif message.text == "Записать тренировку":
        bot.reply_to(message, "Пожалуйста, выберите тип тренировки и введите данные.")
    elif message.text == "Мой прогресс":
        show_progress_menu(bot, message.chat.id)
    else:
        bot.reply_to(message, "Пожалуйста, используйте меню для выбора команд.")

def handle_voice_message(bot, message: Message):
    bot.reply_to(message, "Голосовое сообщение принято!")
