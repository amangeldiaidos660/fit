from telebot import TeleBot
from config import BOT_TOKEN
from handlers import start, handle_menu_command, handle_voice_message, handle_text_message, handle_save_or_cancel
from progress import handle_progress_buttons

bot = TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start_command(message):
    start(bot, message)

@bot.message_handler(content_types=["text"])
def text_command_handler(message):
    if message.text in ["Войти", "Выйти"]:
        handle_menu_command(bot, message)
    elif message.text in ["Сохранить", "Отмена"]:
        handle_save_or_cancel(bot, message)
    else:
        handle_text_message(bot, message)

@bot.message_handler(content_types=["voice"])
def voice_command_handler(message):
    handle_voice_message(bot, message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("progress"))
def progress_buttons_handler(call):
    handle_progress_buttons(bot, call)

if __name__ == "__main__":
    bot.infinity_polling()
