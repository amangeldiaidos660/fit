import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

selected_dates = {"start": None, "end": None} 

BOT_TOKEN = "7777000113:AAHZ-irduLYqc9sK8LwT5eULFrKgTfFpXOI"

bot = telebot.TeleBot(BOT_TOKEN)


keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Войти"), KeyboardButton("Записать тренировку"))
keyboard.add(KeyboardButton("Мой прогресс"))

@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Выберите команду из меню или отправьте голосовое сообщение.",
        reply_markup=keyboard, 
    )

@bot.message_handler(content_types=["text"])
def handle_menu_command(message: Message):
    if message.text == "Войти":
        bot.reply_to(message, "Вы вошли в систему. Что вы хотите сделать дальше?")
    elif message.text == "Записать тренировку":
        bot.reply_to(message, "Пожалуйста, выберите тип тренировки и введите данные.")
    elif message.text == "Мой прогресс":
        show_progress_menu(message.chat.id)
    else:
        bot.reply_to(message, "Пожалуйста, используйте меню для выбора команд.")


@bot.message_handler(content_types=["voice"])
def handle_voice_message(message: Message):
    bot.reply_to(message, "Голосовое сообщение принято!")

def show_progress_menu(chat_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("С", callback_data="progress_start"),
        InlineKeyboardButton("По", callback_data="progress_end")
    )
    keyboard.add(InlineKeyboardButton("Показать прогресс", callback_data="progress_show"))
    bot.send_message(chat_id, "Выберите период для отображения прогресса:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("progress"))
def handle_progress_buttons(call):
    if call.data == "progress_start":
        bot.send_message(call.message.chat.id, "Выберите дату начала (формат: ДД.ММ.ГГГГ):")
        bot.register_next_step_handler(call.message, set_start_date)
    elif call.data == "progress_end":
        bot.send_message(call.message.chat.id, "Выберите дату окончания (формат: ДД.ММ.ГГГГ):")
        bot.register_next_step_handler(call.message, set_end_date)
    elif call.data == "progress_show":
        if selected_dates["start"] and selected_dates["end"]:
            bot.send_message(
                call.message.chat.id,
                f"Выбранный период:\nДата начала: {selected_dates['start']}\nДата окончания: {selected_dates['end']}"
            )
        else:
            bot.send_message(call.message.chat.id, "Пожалуйста, укажите оба значения периода (С и По).")

def set_start_date(message):
    try:
        selected_dates["start"] = validate_date(message.text)
        bot.send_message(message.chat.id, f"Дата начала установлена: {selected_dates['start']}")
        bot.send_message(message.chat.id, "Теперь выберите дату окончания (формат: ДД.ММ.ГГГГ):")
        bot.register_next_step_handler(message, set_end_date)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат даты. Попробуйте снова.")
        bot.register_next_step_handler(message, set_start_date)

def set_end_date(message):
    try:
        selected_dates["end"] = validate_date(message.text)
        bot.send_message(message.chat.id, f"Дата окончания установлена: {selected_dates['end']}")
        bot.send_message(
            message.chat.id,
            f"Выбранный период:\nДата начала: {selected_dates['start']}\nДата окончания: {selected_dates['end']}"
        )
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат даты. Попробуйте снова.")
        bot.register_next_step_handler(message, set_end_date)

def validate_date(date_text):
    return datetime.strptime(date_text, "%d.%m.%Y").date()


bot.infinity_polling()
