import re
import hashlib
from db import check_user_in_db

def auth_bot(bot, chat_id):
    bot.send_message(chat_id, "Пожалуйста, введите вашу почту:")
    bot.register_next_step_handler_by_chat_id(chat_id, validate_email, bot)

def validate_email(message, bot):
    email = message.text
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        bot.send_message(message.chat.id, "Почта принята. Введите ваш пароль:")
        bot.register_next_step_handler_by_chat_id(message.chat.id, validate_password, bot, email=email)
    else:
        bot.send_message(message.chat.id, "Некорректный формат почты. Попробуйте снова:")
        bot.register_next_step_handler_by_chat_id(message.chat.id, validate_email, bot)

def validate_password(message, bot, email):
    password = message.text
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    is_valid, response = check_user_in_db(email, hashed_password, message.chat.id)
    bot.send_message(message.chat.id, response)
    if is_valid:
        bot.send_message(message.chat.id, "Добро пожаловать!")
