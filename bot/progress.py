from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

selected_dates = {"start": None, "end": None}

def show_progress_menu(bot, chat_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("С", callback_data="progress_start"),
        InlineKeyboardButton("По", callback_data="progress_end")
    )
    keyboard.add(InlineKeyboardButton("Показать прогресс", callback_data="progress_show"))
    bot.send_message(chat_id, "Выберите период для отображения прогресса:", reply_markup=keyboard)

def handle_progress_buttons(bot, call):
    if call.data == "progress_start":
        bot.send_message(call.message.chat.id, "Выберите дату начала (формат: ДД.ММ.ГГГГ):")
        bot.register_next_step_handler(call.message, set_start_date, bot)
    elif call.data == "progress_end":
        bot.send_message(call.message.chat.id, "Выберите дату окончания (формат: ДД.ММ.ГГГГ):")
        bot.register_next_step_handler(call.message, set_end_date, bot)
    elif call.data == "progress_show":
        if selected_dates["start"] and selected_dates["end"]:
            bot.send_message(
                call.message.chat.id,
                f"Выбранный период:\nДата начала: {selected_dates['start']}\nДата окончания: {selected_dates['end']}"
            )
        else:
            bot.send_message(call.message.chat.id, "Пожалуйста, укажите оба значения периода (С и По).")

def set_start_date(message, bot):
    try:
        selected_dates["start"] = validate_date(message.text)
        bot.send_message(message.chat.id, f"Дата начала установлена: {selected_dates['start']}")
        bot.send_message(message.chat.id, "Теперь выберите дату окончания (формат: ДД.ММ.ГГГГ):")
        bot.register_next_step_handler(message, set_end_date, bot)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат даты. Попробуйте снова.")
        bot.register_next_step_handler(message, set_start_date, bot)

def set_end_date(message, bot):
    try:
        selected_dates["end"] = validate_date(message.text)
        bot.send_message(message.chat.id, f"Дата окончания установлена: {selected_dates['end']}")
        bot.send_message(
            message.chat.id,
            f"Выбранный период:\nДата начала: {selected_dates['start']}\nДата окончания: {selected_dates['end']}"
        )
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат даты. Попробуйте снова.")
        bot.register_next_step_handler(message, set_end_date, bot)

def validate_date(date_text):
    return datetime.strptime(date_text, "%d.%m.%Y").date()
