import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message

# Токен вашего бота (замените на свой)
BOT_TOKEN = "7777000113:AAHZ-irduLYqc9sK8LwT5eULFrKgTfFpXOI"

bot = telebot.TeleBot(BOT_TOKEN)

# Создаем клавиатуру с меню
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Команда 1"), KeyboardButton("Команда 2"))

# Обработка команды /start
@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Выберите команду из меню или отправьте голосовое сообщение.",
        reply_markup=keyboard,  # Добавляем клавиатуру к сообщению
    )

# Хендлер на текстовые сообщения для обработки команд из меню
@bot.message_handler(content_types=["text"])
def handle_menu_command(message: Message):
    if message.text in ["Команда 1", "Команда 2"]:
        bot.reply_to(message, f"Вы выбрали: {message.text}")
    else:
        bot.reply_to(message, "Пожалуйста, используйте меню для выбора команд.")

# Хендлер для голосовых сообщений
@bot.message_handler(content_types=["voice"])
def handle_voice_message(message: Message):
    bot.reply_to(message, "Голосовое сообщение принято!")

# Хендлер для всего остального
@bot.message_handler(func=lambda message: True)
def handle_unsupported_content(message: Message):
    bot.reply_to(message, "Я принимаю только голосовые сообщения или команды из меню.")

# Запуск бота
bot.infinity_polling()
